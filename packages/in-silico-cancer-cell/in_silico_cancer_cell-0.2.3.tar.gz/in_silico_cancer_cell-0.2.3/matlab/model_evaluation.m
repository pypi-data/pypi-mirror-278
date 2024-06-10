function [NOCs, mean_RMS] = model_evaluation(time_vector_measure, total_curr_meas, total_curr_meas_all, EvK, EvCa, EvCl, Ca_steady_state, F, R, T, N_CRAC1, protocol, cellPhase, NOCs_optimization)
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % Model evaluation
  % input:
  %  * time_vector_measure: time vector of the measurements
  %  * total_curr_meas: measured current at highest input voltage level averaged
  %    over all cells
  %  * total_curr_meas_all: measured current at all input voltage levels averaged
  %    over all cells
  %  * EvK: reversal potential K
  %  * EvCa: reversal potential Ca
  %  * EvCl: reversal potential Cl
  %  * Ca_steady_state: steady state calcium concentration
  %  * F: Faraday constant [As/mol]
  %  * R: gas constant [kgm?/s?molK]
  %  * T: temperature [K]
  %  * N_CRAC1: number of CRAC channels
  %  * protocol: a number between 1 and 6:
  %    - 1 or 2: activation protocol
  %    - 3 or 4: deactivation protocol
  %    - 5 or 6: ramp protocol
  %  * cell_phase: a number between 0 and 1:
  %    0: number of ion channels estimated for G0 phase
  %    1: number of ion channels estimated for G1 phase
  %  * NOCs_optimization: estimated or defined number of channels for each channel type
  % output:
  %  * NOCs_optimization: estimated or defined number of channels for each
  %  channel type (optional, if not defined, predefined values will be used)
  %        NOCs(1):  %KV1.3
  %        NOCs(2):  %Kv3.1
  %        NOCs(3):  %Kv3.4
  %        NOCs(4):  %K7.1
  %        NOCs(5):  %KCa1.1
  %        NOCs(6):  %KCa3.1
  %        NOCs(7):  %TASK1
  %        NOCs(8):  %TRPV
  %        NOCs(9):  %TRPC
  %        NOCs(10): %CLC-2
  %  * mean RMS: averaged root mean square value over all applied voltage steps
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

  %% calcium concentration
  Ca_i = Ca_steady_state;

  % sampling frequency for simulation
  freq = 2000000;
  dt = 1 / freq;
  sprintf('PROTOCOL')
  protocol

  %% specify the number of ion channels for the simulation
  if nargin < 14 % no NOCS given by user

    switch cellPhase
      case 0
        NOCs = [22; 78; 5; 1350; 40; 77; 19; 12; 17; 13]; % NOCs_global G0 phase
      case 1
        NOCs = [20; 90; 54; 558; 15; 63; 10; 13; 12; 11]; % NOCs_global G1 phase
      otherwise
        error('specify cell phase 0 or 1')
    end

  else
    NOCs = NOCs_optimization;
  end

  %% define simulation protocol
  V_hold = -100e-3;
  t_hold = 100e-3;
  pulse_protocol = {};
  test_pulses = [];

  switch protocol
    case {1, 2}
      % activation protocol
      test_pulses = [-40e-3, -30e-3, -20e-3, -10e-3, 0, 10e-3, 20e-3, 30e-3, 40e-3]
      V_initial = -80e-3;
      t_initial = 115.6e-3;
      t_test = 800e-3;
      V_post = -80e-3;
      t_post = 84.4e-3;

    case {3, 4}
      % deactivation protocol
      V_initial = -40e-3;
      t_initial = 155e-3;
      V_initial_2 = 40e-3;
      t_initial_2 = 5000e-3;
      t_test = 4920e-3;
      V_post = -40e-3;
      t_post = 165e-3;
      test_pulses = [-100e-3, -90e-3, -80e-3, -70e-3, -60e-3, -50e-3, -40e-3];

    case {5, 6}
      % ramp protocol
      vektor_ramp = zeros(2064, 2);
      vektor_ramp(1:30, 1) = -0.1;
      vektor_ramp(31:2031, 1) = -0.1:0.00008:0.060;
      vektor_ramp(2032:2064, 1) = -0.1;
      vektor_ramp(:, 2) = 0.01;
      k = 1;

      for i = 1:length(vektor_ramp)
        pulse_protocol(1, k) = {vektor_ramp(i, 1)};
        pulse_protocol(1, k + 1) = {vektor_ramp(i, 2)};
        k = k + 2;
      end

      test_pulses = 1;
  end

  %% define HMM models
  CRAC1_model = CRAC1();
  Kv_1_3_model = Kv_1_3();
  Kv_3_1_model = Kv_3_1();
  Kv_3_4_model = Kv_3_4(F, R, T);
  Kv_7_1_model = Kv_7_1(F, R, T);
  KCa_1_1_model = KCa_1_1(Ca_i);
  KCa_3_1_model = KCa_3_1(Ca_i);
  TASK1_model = TASK1(F, R, T);
  CLC_2_model = CLC_2(F, R, T);

  %% simulate all HMM models
  for V_test_index = 1:length(test_pulses)
    V_test = test_pulses(V_test_index);

    if protocol == 1 || protocol == 2
      % activation pulse protocol
      pulse_protocol = {V_hold, t_hold, V_initial, t_initial, V_test, t_test, V_post, t_post};
    elseif protocol == 3 || protocol == 4
      % deactivation pulse protocol
      pulse_protocol = {V_hold, t_hold, V_initial, t_initial, V_initial_2, t_initial_2, V_test, t_test, V_post, t_post};
    elseif protocol == 5 || protocol == 6
      % ramp pulse protocol
      pulse_protocol
    end

    [~, current_KV_1_3i(:, V_test_index), time_vector] = simulate_pulse_protocol(Kv_1_3_model, dt, pulse_protocol, EvK, 0, 1);
    [~, current_KV_3_1i(:, V_test_index)] = simulate_pulse_protocol(Kv_3_1_model, dt, pulse_protocol, EvK, 0, 1);
    [~, current_KV_3_4i(:, V_test_index)] = simulate_pulse_protocol(Kv_3_4_model, dt, pulse_protocol, EvK, 0, 1);
    [~, current_KV_7_1i(:, V_test_index)] = simulate_pulse_protocol(Kv_7_1_model, dt, pulse_protocol, EvK, 0, 1);
    [~, current_KCa_1_1i(:, V_test_index)] = simulate_pulse_protocol(KCa_1_1_model, dt, pulse_protocol, EvK, Ca_i, 1);
    [~, current_KCa_3_1i(:, V_test_index)] = simulate_pulse_protocol(KCa_3_1_model, dt, pulse_protocol, EvK, Ca_i, 0);
    [~, current_TASK1i(:, V_test_index)] = simulate_pulse_protocol(TASK1_model, dt, pulse_protocol, EvK, Ca_i, 1);
    [~, current_CRAC1i(:, V_test_index)] = simulate_pulse_protocol(CRAC1_model, dt, pulse_protocol, EvCa, Ca_i, 1);
    [~, current_TRPV3i(V_test_index, :)] = simulate_pulse_protocol_TRPV(dt, pulse_protocol, EvCa);
    [~, current_TRPC6i(V_test_index, :)] = simulate_pulse_protocol_TRPC(dt, pulse_protocol, EvCa);
    [~, current_CLC_2i(V_test_index, :)] = simulate_pulse_protocol(CLC_2_model, dt, pulse_protocol, EvCl, 0, 1);
    close all

    C_full_i(:, :, V_test_index) = [current_KV_1_3i(:, V_test_index)';
                                    current_KV_3_1i(:, V_test_index)';
                                    current_KV_3_4i(:, V_test_index)';
                                    current_KV_7_1i(:, V_test_index)';
                                    current_KCa_1_1i(:, V_test_index)';
                                    current_KCa_3_1i(:, V_test_index)';
                                    current_TASK1i(:, V_test_index)';
                                    current_TRPV3i(V_test_index, :);
                                    current_TRPC6i(V_test_index, :);
                                    current_CLC_2i(V_test_index, :)];
  end

  %% plot measured and simulated whole-cell current
  figure
  hold on
  i_v = [];
  sprintf('TEST PULSE')
  length(test_pulses)

  for V_test_index = 1:length(test_pulses)

    if protocol == 1 || protocol == 2
      %activation protocol
      plot(time_vector - t_hold, NOCs' * C_full_i(:, :, V_test_index) * 1e9 + N_CRAC1 * current_CRAC1i(:, V_test_index)' * 1e9, 'b', 'Color', [0, 0.4470, 0.7410], 'linewidth', 1.5);
      i_v(V_test_index, :) = [NOCs' * C_full_i(:, :, V_test_index) * 1e9 + N_CRAC1 * current_CRAC1i(:, V_test_index)' * 1e9]';
    else
      % deactivation protocol
      if protocol == 3 || protocol == 4
        x_sub = 10098;
        % ramp protocol
      elseif protocol == 5 || protocol == 6
        x_sub = 20001;
      end

      k = 1;

      for ii = 1:x_sub:length(current_TRPC6i) - 1
        y(k, V_test_index) = (NOCs(:, 1)' * C_full_i(:, ii, V_test_index) + N_CRAC1 * current_CRAC1i(ii, V_test_index));
        x(k, V_test_index) = time_vector(1, ii);
        k = k + 1;
      end

      plot(x, y(:, V_test_index) * 1e9, 'b', 'Color', [0, 0.4470, 0.7410], 'linewidth', 1.5)
    end

    grid on
  end

  % activation
  if protocol == 1 || protocol == 2
    i_v = i_v';
    plot(time_vector_measure, total_curr_meas_all', '-k', 'linewidth', 0.5)
    %     plot(time_vector_measure,total_curr_meas_all(:,6)','-k','linewidth',0.5)
    %     plot(time_vector_measure,total_curr_meas_all(:,7)','-k','linewidth',0.5)
    %     plot(time_vector_measure,total_curr_meas_all(:,8)','-k','linewidth',0.5)
    %     plot(time_vector_measure,total_curr_meas_all(:,9)','-k','linewidth',0.5)
    %     plot(time_vector_measure,total_curr_meas_all(:,1)','-k','linewidth',0.5)
    %     plot(time_vector_measure,total_curr_meas_all(:,2)','-k','linewidth',0.5)
    %     plot(time_vector_measure,total_curr_meas_all(:,3)','-k','linewidth',0.5)
    %     plot(time_vector_measure,total_curr_meas_all(:,4)','-k','linewidth',0.5)
    axis([-0.01 1.01 -3 * 10^-1 4 * 10^-1])
  end

  % deactivation
  if protocol == 3 || protocol == 4
    plot(time_vector_measure + t_hold, total_curr_meas_all', '-k', 'linewidth', 0.5)
    %     plot(time_vector_measure+t_hold,total_curr_meas_all(:,2)','-k','linewidth',0.5)
    %     plot(time_vector_measure+t_hold,total_curr_meas_all(:,3)','-k','linewidth',0.5)
    %     plot(time_vector_measure+t_hold,total_curr_meas_all(:,4)','-k','linewidth',0.5)
    %     plot(time_vector_measure+t_hold,total_curr_meas_all(:,5)','-k','linewidth',0.5)
    %     plot(time_vector_measure+t_hold,total_curr_meas_all(:,6)','-k','linewidth',0.5)
    %     plot(time_vector_measure+t_hold,total_curr_meas_all(:,7)','-k','linewidth',0.5)
    axis([-0.01 11 -5 * 10^-1 5 * 10^-1])
  end

  % ramp 20s
  if protocol == 5 || protocol == 6
    plot(time_vector_measure, total_curr_meas_all * 1e-9', '-k', 'linewidth', 0.5)
    axis([-0.01 20.5 -4 * 10^-1 8 * 10^-1])
  end

  ylabel('Whole-cell current [nA]', 'FontSize', 16)
  xlabel('Time [s]', 'FontSize', 16)
  grid on

  %% current-voltage curve activation measurements
  if protocol == 1 || protocol == 2
    t_steady = 0.711;
    t_steady_index = find(time_vector_measure(:, 1) == t_steady)
    voltage_levels = [-40, -30, -20, -10, 0, 10, 20, 30, 40];
    measured_currents = [total_curr_meas_all(t_steady_index, 1), total_curr_meas_all(t_steady_index, 2), total_curr_meas_all(t_steady_index, 3), total_curr_meas_all(t_steady_index, 4), total_curr_meas_all(t_steady_index, 5), ...
                           total_curr_meas_all(t_steady_index, 6), total_curr_meas_all(t_steady_index, 7), total_curr_meas_all(t_steady_index, 8), total_curr_meas_all(t_steady_index, 9)];

    figure
    plot(voltage_levels, measured_currents, '--', 'Color', [0.224, 0.224, 0.224], 'linewidth', 1.5)
    hold on
    plot(voltage_levels, i_v(1800000, 1:9), 'Color', [0, 0.4470, 0.7410], 'linewidth', 1.5);

    ylabel('Whole-cell current [nA]', 'FontSize', 16)
    xlabel('Voltage [mV]', 'FontSize', 16)
    legend('measured', 'simulated')
    axis([-40 40 -2 * 10^-1 4 * 10^-1])
    grid on
  end

  %% RMS of whole-cell current curves activation

  if protocol == 1 || protocol == 2
    m_all(:, 5) = total_curr_meas_all(:, 5)';
    m_all(:, 6) = total_curr_meas_all(:, 6)';
    m_all(:, 7) = total_curr_meas_all(:, 7)';
    m_all(:, 8) = total_curr_meas_all(:, 8)';
    m_all(:, 9) = total_curr_meas_all(:, 9)';
    m_all(:, 1) = total_curr_meas_all(:, 1)';
    m_all(:, 2) = total_curr_meas_all(:, 2)';
    m_all(:, 3) = total_curr_meas_all(:, 3)';
    m_all(:, 4) = total_curr_meas_all(:, 4)';

    i_v_nA = i_v;
    i_v_nA_cut = i_v_nA(200000:2200000, :);
    i_v_nA_downsamp = i_v_nA_cut(1:100:end - 1, :);
    lower_samp_range = 0.01 * length(total_curr_meas);
    upper_samp_range = 0.9 * length(total_curr_meas);

    for V_test_index = 1:length(test_pulses)

      for i = 1:length(i_v_nA_downsamp)

        sub(i, V_test_index) = (i_v_nA_downsamp(i, V_test_index) - m_all(i, V_test_index))^2;
      end

    end

    for V_test_index = 1:length(test_pulses)
      RMS(1, V_test_index) = sqrt(sum(sub(lower_samp_range:upper_samp_range - 1, V_test_index)) / (upper_samp_range - lower_samp_range));
    end

    mean_RMS = sum(RMS) / 9
  end

  %% RMS deactivation

  if protocol == 3 || protocol == 4

    m_all(:, 1) = total_curr_meas_all(:, 1)';
    m_all(:, 2) = total_curr_meas_all(:, 2)';
    m_all(:, 3) = total_curr_meas_all(:, 3)';
    m_all(:, 4) = total_curr_meas_all(:, 4)';
    m_all(:, 5) = total_curr_meas_all(:, 5)';
    m_all(:, 6) = total_curr_meas_all(:, 6)';
    m_all(:, 7) = total_curr_meas_all(:, 7)';

    for V_test_index = 1:length(test_pulses)

      for i = 1:length(y)
        sub(i, V_test_index) = (y(i, V_test_index) * 10^9 - m_all(i, V_test_index))^2;
      end

    end

    for V_test_index = 1:length(test_pulses)
      RMS(1, V_test_index) = sqrt(sum(sub(:, V_test_index)) / length(total_curr_meas_all(:, 1)'))
    end

    mean_RMS = sum(RMS) / 7
  end

  %% RMS voltage-ramp

  if protocol == 5 || protocol == 6

    for V_test_index = 1

      for i = 1:length(y)

        sub(i, V_test_index) = (y(i, V_test_index) * 10^9 - total_curr_meas_all(i, 1) * 1e-9)^2;
      end

    end

    for V_test_index = 1
      mean_RMS(1, V_test_index) = sqrt(sum(sub(:, V_test_index)) / length(total_curr_meas_all))
    end

  end

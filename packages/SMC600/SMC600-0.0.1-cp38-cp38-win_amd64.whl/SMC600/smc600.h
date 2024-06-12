#include <iostream>
#include <string>
#include <vector>

using namespace std;

#include "LTSMC.h"

static short board_init_e(unsigned short CardNo, unsigned short type, char *pconnectstring, unsigned long dwBaudRate) {
    return smc_board_init(CardNo, type, pconnectstring, dwBaudRate) > 0 ? 0 : 71;
}

static short board_reset_e(unsigned short CardNo) {
    return smc_board_reset(CardNo);
}

static short board_close_e(unsigned short CardNo) {
    return smc_board_close(CardNo);
}

static unsigned long get_card_version_list_e(unsigned short CardNo) {
    unsigned long card_version_list;
    short ret = smc_get_card_version(CardNo, &card_version_list);

    if (ret != 0) return 71;
    return card_version_list;
}

static short set_alm_mode_e(unsigned short CardNo, unsigned short axis, unsigned short enable, unsigned short alm_logic,
                            unsigned short alm_action) {
    return smc_set_alm_mode(CardNo, axis, enable, alm_logic, alm_action);
}

static short write_sevon_pin_e(unsigned short CardNo, unsigned short axis, unsigned short on_off) {
    return smc_write_sevon_pin(CardNo, axis, on_off);
}

static short set_pulse_outmode_e(unsigned short CardNo, unsigned short axis, unsigned short outmode) {
    return smc_set_pulse_outmode(CardNo, axis, outmode);
}

static short
set_profile_e(unsigned short CardNo, unsigned short axis, double Min_Vel, double Max_Vel, double Tacc, double Tdec,
              double Stop_Vel) {
    return smc_set_profile_unit(CardNo, axis, Min_Vel, Max_Vel, Tacc, Tdec, Stop_Vel);
}

static short set_s_profile_e(unsigned short CardNo, unsigned short axis, unsigned short s_mode, double s_para) {
    return smc_set_s_profile(CardNo, axis, s_mode, s_para);
}

static short set_homemode_e(unsigned short CardNo, unsigned short axis, unsigned short home_dir, double vel_mode,
                            unsigned short mode, unsigned short EZ_count) {
    return smc_set_homemode(CardNo, axis, home_dir, vel_mode, mode, EZ_count);
}

static short home_move_e(unsigned short CardNo, unsigned short axis) {
    return smc_home_move(CardNo, axis);
}

static short pmove_e(unsigned short CardNo, unsigned short axis, long Dist, unsigned short posi_mode) {
    return smc_pmove_unit(CardNo, axis, Dist, posi_mode);
}

static short check_done(unsigned short CardNo, unsigned short axis) {
    return smc_check_done(CardNo, axis);
}

static double get_position(unsigned short CardNo, unsigned short axis) {
    double pos = 0;
    short ret = smc_get_position_unit(CardNo, axis, &pos);
    return pos;
}

static short set_position_e(unsigned short CardNo, unsigned short axis, double current_position) {
    return smc_set_position_unit(CardNo, axis, current_position);
}

static short stop(unsigned short CardNo, unsigned short axis, unsigned short stop_mode) {
    return smc_stop(CardNo, axis, stop_mode);
}

static short emg_stop_e(unsigned short CardNo) {
    return smc_emg_stop(CardNo);
}

static short update_target_position_e(unsigned short CardNo, unsigned short axis, long dst) {
    return smc_update_target_position_unit(CardNo, axis, dst);
}

static short reset_target_position_e(unsigned short CardNo, unsigned short axis, long dist) {
    return smc_reset_target_position_unit(CardNo, axis, dist);
}

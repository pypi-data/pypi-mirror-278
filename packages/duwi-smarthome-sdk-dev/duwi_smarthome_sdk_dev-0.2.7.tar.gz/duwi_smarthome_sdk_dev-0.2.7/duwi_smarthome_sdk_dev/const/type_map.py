# device_type
type_map = {
    "switch": {
        "1-002": "on",
        "1-003": "on",
        "1-005": "on",
        "1-006": "on",
        "107-001": "on",
    },
    "light": {
        "1-001": "on",
        "1-004": "on",
        "3-001": "dim",
        "3-002": "temp",
        "3-003": "dim_temp",
        "3-004": "rgbw",
        "3-005": "rgb",
        "3-006": "rgbcw",
    },
    "cover": {
        "4-001": "roll",
        "4-002": "roll",
        "4-003": "shutter",
        "4-004": "shutter",
    },
}

group_type_map = {
    "switch": {
        "breaker": "on",
    },
    "light": {
        "light": "dim",
        "color": "temp",
        "lightcolor": "dim_temp",
        "rgbw": "rgbw",
        "rgb": "rgb",
    },
    "cover": {
        "retractable": "roll",
        "roller": "roll",
    },
}

media_type_map = {
    "8-001-001": "hua_ersi_music",
    "8-001-002": "xiang_wang_music_s7_mini_3s",
    "8-001-003": "xiang_wang_music_s8",
    "8-001-004": "sheng_bi_ke_music",
    "8-001-005": "bo_sheng_music",
    "8-001-006": "sonos_music",
}

sensor_type_map = {
    "7-001-001": ["temperature"],
    "7-002-001": ["humidity"],
    "7-003-001": ["light"],
    "7-004-001": ["formaldehyde"],
    "7-005-001": ["pm25"],
    "7-006-001": ["carbon_dioxide"],
    "7-007-001": ["air_quality"],
    "7-008-001": ["human"],
    "7-008-002": ["human"],
    "7-008-003": ["human", "light"],
    "7-009-001": ["trigger"],
    "7-009-002": ["human"],
    "7-009-003": ["human", "light"],
    "7-009-004": ["trigger"],
    "7-009-005": ["trigger"],
    "7-009-006": ["trigger"],
    "7-009-007": ["trigger"],
    "7-009-008": ["trigger"],
    "7-009-009": ["human"],
    "7-009-010": ["human"],
    "7-010-001": ["carbon_monoxide"],
    "7-011-001": ["tvoc"],
    "7-012-001": ["temperature", "humidity", "tvoc", "pm25", "formaldehyde", "carbon_dioxide", "pm10"],
    "7-012-002": ["carbon_monoxide"],
    "7-013-001": ["light", "human"],
}

havc_type_map = {
    "5-001-001": {
        "ac_set_temp_range": [15, 35],
        "ac_mode": ["auto", "cold", "hot", "fan", "wet", "air"],
        "ac_wind_speed": ["auto", "super_strong", "super_high", "high", "mid", "low", "super_low", "super_quiet"],
        "ac_wind_direction": ["auto", "stop", "swing", "up_down", "left_right"],
        "ac_temp_adjust": ["up", "down"],
    },
    "5-001-002": {
        "ac_set_temp_range": [10, 30],
        "ac_mode": ["cold", "hot"],
        "ac_wind_speed": ["auto", "high", "mid", "low"],
        "ac_temp_adjust": ["up", "down"],
    },
    "5-001-003": {
        "ac_set_temp_range": [16, 32],
        "ac_mode": ["cold", "hot", "fan", "wet"],
        "ac_wind_speed": ["auto", "high", "mid", "low"],
        "ac_temp_adjust": ["up", "down"],
    },
    "5-001-004": {
        "ac_set_temp_range": [15, 35],
        "ac_mode": ["auto", "cold", "hot", "fan", "wet"],
        "ac_wind_speed": ["auto", "high", "mid", "low"],
        "ac_temp_adjust": ["up", "down"],
    },
    "5-001-005": {
        "ac_set_temp_range": [15, 45],
        "ac_mode": ["cold", "hot", "fan", "wet", "heat", "mix"],
        "ac_wind_speed": ["auto", "high", "mid", "low"],
        "ac_temp_adjust": ["up", "down"],
    },
    "5-001-006": {
        "ac_set_temp_range": [5, 35],
        "ac_mode": ["cold", "hot", "fan"],
        "ac_wind_speed": ["auto", "high", "mid", "low"],
        "ac_temp_adjust": ["up", "down"],
    },
    "5-001-007": {
        "ac_set_temp_range": [5, 35],
        "ac_mode": ["cold", "hot", "fan", "heat", "mix"],
        "ac_wind_speed": ["auto", "high", "mid", "low"],
        "ac_temp_adjust": ["up", "down"],
    },
    "5-001-008": {
        "ac_set_temp_range": [5, 35],
        "ac_mode": ["cold", "hot", "fan", "heat", "mix"],
        "ac_wind_speed": ["auto", "high", "mid", "low"],
        "ac_temp_adjust": ["up", "down"],
    },
    "5-001-009": {
        "ac_set_temp_range": [10, 32],
        "ac_mode": ["cold", "hot", "fan", "wet", "heat", "mix"],
        "ac_wind_speed": ["auto", "high", "mid", "low"],
        "ac_temp_adjust": ["up", "down"],
    },
    "5-001-010": {
        "ac_set_temp_range": [5, 30],
        "ac_mode": ["cold", "hot", "fan", "wet", "auto", "heat", "mix", "wet_reheat"],
        "ac_wind_speed": ["auto", "super_high", "high", "mid_high", "mid", "mid_low", "low", "super_low"],
        "ac_temp_adjust": ["up", "down"],
    },
    "5-001-011": {
        "ac_set_temp_range": [10, 30],
        "ac_mode": ["cold", "hot", "fan", "wet", "auto"],
        "ac_wind_speed": ["auto", "high", "mid_high", "mid", "mid_low", "low", "super_low"],
        "ac_temp_adjust": ["up", "down"],
    },
    "5-001-012": {
        "ac_set_temp_range": [5, 35],
        "ac_mode": ["cold", "hot", "fan", "wet", "heat", "mix"],
        "ac_wind_speed": ["auto", "high", "mid", "low"],
        "ac_temp_adjust": ["up", "down"],
    },
    "5-001-013": {
        "ac_set_temp_range": [10, 35],
        "ac_mode": ["cold", "hot", "fan", "wet", "heat", "mix"],
        "ac_wind_speed": ["auto", "high", "mid", "low"],
        "ac_temp_adjust": ["up", "down"],
    },
    "5-001-014": {
        "ac_set_temp_range": [10, 35],
        "ac_mode": ["cold", "hot", "fan", "wet", "heat", "mix"],
        "ac_wind_speed": ["auto", "high", "mid", "low"],
        "ac_temp_adjust": ["up", "down"],
    },
    "5-001-015": {
        "ac_set_temp_range": [16, 30],
        "ac_mode": ["cold", "hot", "fan", "wet", "heat", "mix"],
        "ac_wind_speed": ["auto", "high", "mid", "low"],
        "ac_temp_adjust": ["up", "down"],
    },
    "5-001-016": {
        "ac_set_temp_range": [5, 45],
        "ac_mode": ["cold", "hot", "fan", "wet", "heat", "mix"],
        "ac_wind_speed": ["auto", "high", "mid", "low"],
        "ac_temp_adjust": ["up", "down"],
    },
    "5-001-017": {
        "ac_set_temp_range": [16, 32],
        "ac_mode": ["cold", "hot", "fan", "wet", "humidify"],
        "ac_wind_speed": ["auto", "high", "mid", "low"],
        "ac_temp_adjust": ["up", "down"],
    },
    "5-001-018": {
        "ac_set_temp_range": [19, 30],
        "ac_mode": ["cold", "hot", "fan", "wet"],
        "ac_wind_speed": ["high", "mid", "low"],
        "ac_temp_adjust": ["up", "down"],
    },
    "5-001-019": {
        "ac_set_temp_range": [16, 30],
        "ac_mode": ["auto", "cold", "hot", "fan", "wet"],
        "ac_wind_speed": ["auto", "high", "mid", "low"],
        "ac_temp_adjust": ["up", "down"],
    },
    "5-001-020": {
        "ac_set_temp_range": [16, 32],
        "ac_mode": ["auto", "cold", "hot", "fan", "wet"],
        "ac_wind_speed": ["auto", "high", "mid", "low"],
        "ac_temp_adjust": ["up", "down"],
    },
    "5-001-021": {
        "ac_set_temp_range": [16, 30],
        "ac_mode": ["auto", "cold", "hot", "fan", "wet"],
        "ac_wind_speed": ["auto", "high", "mid", "low"],
        "ac_temp_adjust": ["up", "down"],
    },
    "5-001-022": {
        "ac_set_temp_range": [17, 30],
        "ac_mode": ["auto", "cold", "hot", "fan", "wet"],
        "ac_wind_speed": ["auto", "super_high", "high", "mid_high", "mid", "mid_low", "low", "super_low"],
        "ac_temp_adjust": ["up", "down"],
    },
    "5-001-023": {
        "ac_set_temp_range": [17, 30],
        "ac_mode": ["auto", "cold", "hot", "fan", "wet"],
        "ac_wind_speed": ["auto", "high", "mid", "low"],
        "ac_temp_adjust": ["up", "down"],
    },
    "5-001-024": {
        "ac_set_temp_range": [10, 32],
        "ac_mode": ["cold", "hot", "fan", "wet"],
        "ac_wind_speed": ["high", "mid", "low"],
    },
    "5-001-025": {
        "ac_set_temp_range": [10, 32],
        "ac_mode": ["cold", "hot", "fan"],
        "ac_wind_speed": ["auto", "super_high", "high", "mid", "low", "super_low"],
    },
    "5-001-026": {
        "ac_set_temp_range": [17, 35],
        "ac_mode": ["cold", "hot", "fan", "wet"],
        "ac_wind_speed": ["super_high", "high", "mid", "low"],
    },
    "5-001-027": {
        "ac_set_temp_range": [16, 32],
        "ac_mode": ["cold", "hot", "fan", "wet"],
        "ac_wind_speed": ["high", "mid", "low"],
    },
    "5-001-028": {
        "ac_set_temp_range": [5, 45],
        "ac_mode": ["cold", "hot", "wet"],
        "ac_wind_speed": ["auto", "high", "mid", "low"],
    },
    "5-001-029": {
        "ac_set_temp_range": [17, 30],
        "ac_mode": ["auto", "super_high", "high", "mid_high", "mid", "mid_low", "low", "super_low"],
        "ac_wind_speed": ["auto", "high", "mid", "low"],
    },
    "5-001-030": {
        "ac_set_temp_range": [17, 30],
        "ac_mode": ["auto", "cold", "hot", "fan", "wet"],
        "ac_wind_speed": ["auto", "high", "mid", "low"],
    },
    "5-001-031": {
        "ac_set_temp_range": [16, 30],
        "ac_mode": ["auto", "cold", "hot", "fan", "wet"],
        "ac_wind_speed": ["auto", "super_high", "high", "mid", "low", "super_low"],
    },
    "5-001-032": {
        "ac_set_temp_range": [16, 30],
        "ac_mode": ["cold", "hot", "fan", "wet"],
        "ac_wind_speed": ["auto", "high", "mid", "low", "super_low", "stop"],
    },

    "5-002-001": {
        "fh_set_temp_range": [10, 30],
        "fh_temp_adjust": ["up", "down"],
    },
    "5-002-002": {
        "fh_set_temp_range": [5, 35],
        "fh_temp_adjust": ["up", "down"],
    },
    "5-002-003": {
        "fh_set_temp_range": [5, 35],
        "fh_temp_adjust": ["up", "down"],
    },
    "5-002-004": {
        "fh_set_temp_range": [5, 35],
        "fh_temp_adjust": ["up", "down"],
    },
    "5-002-005": {
        "fh_set_temp_range": [10, 32],
        "fh_temp_adjust": ["up", "down"],
    },
    "5-002-006": {
        "fh_set_temp_range": [16, 45],
        "fh_temp_adjust": ["up", "down"],
    },
    "5-002-007": {
        "fh_set_temp_range": [16, 45],
        "fh_temp_adjust": ["up", "down"],
    },
    "5-002-008": {
        "fh_set_temp_range": [16, 45],
        "fh_temp_adjust": ["up", "down"],
    },
    "5-002-009": {
        "fh_set_temp_range": [16, 32],
        "fh_temp_adjust": ["up", "down"],
    },
    "5-002-010": {
        "fh_set_temp_range": [0, 100],
        "fh_temp_adjust": ["up", "down"],
        "fh_real_humidity": True
    },
    "5-002-011": {
        "fh_set_temp_range": [16, 32],
        "fh_temp_adjust": ["up", "down"],
        "fh_real_humidity": True
    },
    "5-002-012": {
        "fh_set_temp_range": [16, 32],
        "fh_temp_adjust": ["up", "down"],
    },
    "5-002-013": {
        "fh_set_temp_range": [10, 32],
        "fh_temp_adjust": ["up", "down"],
        "fh_real_humidity": True
    },
    "5-002-014": {
        "fh_set_temp_range": [17, 35],
        "fh_temp_adjust": ["up", "down"],
    },
    "5-002-015": {
        "fh_set_temp_range": [5, 35],
        "fh_temp_adjust": ["up", "down"],
    },
    "5-002-016": {
        "fh_set_temp_range": [5, 35],
        "fh_temp_adjust": ["up", "down"],
    },

    "5-003-001": {
        "fa_wind_speed": ["auto", "high", "mid", "low"],
        "fa_set_humidity_range": [20, 95],
        "fa_humidity_adjust": ["up", "down"],
        "fa_real_temp": True
    },
    "5-003-002": {
        "fa_wind_speed": ["auto", "high", "mid", "low"],
        "fa_set_humidity_range": [20, 95],
        "fa_humidity_adjust": ["up", "down"],
        "fa_real_temp": True
    },
    "5-003-003": {
        "fa_wind_speed": ["auto", "high", "mid", "low"],
        "fa_real_temp": True
    },
    "5-003-004": {
        "fa_wind_speed": ["high", "mid", "low", "stop"],
        "fa_work_mode": ["auto", "manual", "timing"],
        "fa_real_temp": True
    },
    "5-003-005": {
        "fa_wind_speed": ["high", "mid", "low", "stop"],
    },
    "5-003-006": {
        "fa_wind_speed": ["high", "mid", "low"],
        "fa_work_mode": ["heat_exchange", "common", "indoor_loop", "outdoor_loop"],
    },
    "5-003-007": {
        "fa_wind_speed": ["high", "mid", "low", "stop"],
        "fa_work_mode": ["manual", "timing"],
        "fa_real_temp": True
    },
    "5-003-008": {
        "fa_wind_speed": ["high", "mid", "low"],
    },
    "5-003-009": {
        "fa_wind_speed": ["air", "clean", "wet"],
        "fa_set_humidity_range": [0, 100],
        "fa_work_mode": ["auto", "manual", "timing"],
        "fa_real_temp": True
    },
    "5-003-010": {
        "fa_wind_speed": ["auto", "super_strong", "super_high", "high", "mid", "low", "super_low", "stop"],
        "fa_real_temp": True
    },
    "5-003-011": {
        "fa_wind_speed": ["auto", "high", "mid", "low", "super_low", "stop"],
        "fa_work_mode": ["air", "wet"],
    },
    "5-003-012": {
        "fa_wind_speed": ["high", "mid", "low", "stop"],
    },
    "5-003-013": {
        "fa_wind_speed": ["indoor_loop", "fresh", "fresh_wet", "wet"],
        "fa_real_temp": True
    },
    "5-003-014": {
        "fa_wind_speed": ["high", "mid", "low", "stop"],
        "fa_real_temp": True
    },
    "5-003-015": {
        "fa_wind_speed": ["high", "mid", "low"],
    },
    "5-003-016": {
        "fa_wind_speed": ["high", "mid", "low"],
    },
    "5-003-017": {
        "fa_wind_speed": ["high", "low"],
        "fa_real_temp": True
    },
    "5-003-018": {
        "fa_wind_speed": ["high", "low"],
        "fa_work_mode": ["fresh", "wet"],
        "fa_set_humidity_range": [0, 100],
    },
    "5-003-019": {
        "fa_wind_speed": ["high", "mid", "low", "stop"],
        "fa_real_temp": True
    },
    "5-003-020": {
        "fa_wind_speed": ["extreme_strong", "super_high", "high", "mid", "low", "super_low"],
        "fa_set_humidity_range": [40, 90],
        "fa_work_mode": ["auto", "manual", "program"],
        "fa_real_temp": True
    },
    "5-003-021": {
        "fa_wind_speed": ["auto", "high", "low"],
        "fa_set_humidity_range": [30, 70],
        "fa_work_mode": ["wet", "ventilate"],
        "fa_real_temp": True
    },
    "5-003-022": {
        "fa_wind_speed": ["high", "mid", "low"],
        "fa_work_mode": ["high", "mid", "low"],
        "fa_set_humidity_range": [30, 70],
    },
    "5-003-023": {
        "fa_wind_speed": ["high", "mid", "low", "stop"],
        "fa_real_temp": True
    },
    "5-003-024": {
        "fa_wind_speed": ["high", "low"],
    },
    "5-003-025": {
        "fa_wind_speed": ["high", "low"],
        "fa_work_mode": ["exhaust", "heat_exchange", "smart", "powerful"],
        "fa_real_temp": True
    },
    "5-003-026": {
        "fa_wind_speed": ["high", "low"],
        "fa_work_mode": ["exhaust", "heat_exchange", "smart", "powerful", "cold_room", "heat_room"],
        "fa_real_temp": True
    },
    "5-003-027": {
        "fa_wind_speed": ["super_high", "high", "mid", "low"],
        "fa_work_mode": ["auto", "timing", "exhaust", "fresh", "energy_recycle", "night", "holiday"],
        "fa_real_temp": True
    },
    "5-003-028": {
        "fa_wind_speed": ["auto", "high", "mid", "low", "super_low", "stop"],
        "fa_work_mode": ["auto", "manual", "timing", "sleep"],
        "fa_real_temp": True
    },
    "5-003-029": {
        "fa_wind_speed": ["high", "mid", "low", "stop"],
        "fa_work_mode": ["auto", "manual", "timing", "sleep"],
        "fa_real_temp": True
    },
    "5-003-030": {
        "fa_wind_speed": ["high", "mid", "low", "stop"],
        "fa_set_humidity_range": [10, 95],
        "fa_work_mode": ["indoor_loop", "fresh", "fresh_wet", "wet"],
        "fa_real_temp": True
    },
    "5-003-031": {
        "fa_wind_speed": ["high", "mid", "low"],
        "fa_work_mode": ["auto", "manual", "night", "holiday"],
        "fa_real_temp": True
    },
    "5-003-032": {
        "fa_wind_speed": ["high", "low"],
        "fa_set_humidity_range": [0, 100],
        "fa_work_mode": ["fresh", "wet"],
        "fa_real_temp": True
    },
    "5-003-033": {
        "fa_wind_speed": ["high", "mid", "low", "super_low", "stop"],
        "fa_work_mode": ["auto", "manual", "timing", "sleep"],
        "fa_real_temp": True
    },
    "5-003-034": {
        "fa_set_humidity_range": [0, 100],
        "fa_work_mode": ["auto", "fresh", "clean", "wet"],
        "fa_real_temp": True
    },
    "5-003-035": {
        "fa_wind_speed": ["high", "mid", "low"],
        "fa_real_temp": True
    },
    "5-003-036": {
        "fa_wind_speed": ["super_high", "high", "mid", "low", "super_low", "stop"],
        "fa_work_mode": ["fresh", "clean", "cold_room", "sleep", "smart", "powerful"],
        "fa_real_temp": True
    },
    "5-003-037": {
        "fa_wind_speed": ["high", "mid", "low"],
        "fa_work_mode": ["night", "holiday"],
    },
    "5-003-038": {
        "fa_set_humidity_range": [0, 100],
    },
    "5-003-039": {
        "fa_wind_speed": ["auto", "extreme_strong", "super_high", "high", "mid", "low", "super_low", "super_quiet"],
        "fa_work_mode": ["auto", "exhaust", "heat_exchange", "indoor_loop", "fresh", "pass"],
        "fa_real_temp": True
    },
    "5-003-040": {
        "fa_wind_speed": ["extreme_strong", "super_high", "high", "mid", "low", "super_low", "super_quiet"],
    },
    "5-003-041": {
        "fa_wind_speed": ["auto", "high", "mid", "low"],
        "fa_work_mode": ["auto", "manual", "timing"],
        "fa_real_temp": True
    },
    "5-003-042": {
        "fa_wind_speed": ["high", "low"],
    },
    "5-003-043": {
        "fa_wind_speed": ["high", "mid", "low"],
    },
    "5-003-044": {
        "fa_wind_speed": ["high", "mid", "low", "stop"],
        "fa_work_mode": ["auto", "manual", "timing"],
        "fa_real_temp": True
    },
    "5-003-045": {
        "fa_wind_speed": ["high", "mid", "low", "stop"],
        "fa_work_mode": ["auto", "manual", "timing"],
        "fa_real_temp": True
    },
    "5-003-046": {
        "fa_wind_speed": ["high", "mid", "low", "stop"],
        "fa_work_mode": ["auto", "manual", "timing"],
    },
    "5-003-047": {
        "fa_wind_speed": ["high", "mid", "low", "stop"],
        "fa_work_mode": ["manual", "timing"],
    },
    "5-003-048": {
        "fa_wind_speed": ["high", "mid", "low"],
        "fa_work_mode": ["auto", "manual", "sleep"],
    },
    "5-003-049": {
        "fa_wind_speed": ["auto", "super_high", "high", "mid", "low", "super_low"],
        "fa_work_mode": ["auto", "manual"],
    },
    "5-003-050": {
        "fa_wind_speed": ["auto", "high", "mid", "low", "super_low", "stop"],
        "fa_work_mode": ["high", "mid", "low"],
    },
    "5-003-051": {
        "fa_wind_speed": ["high", "mid", "low"],
        "fa_real_temp": True
    },
    "5-003-052": {
        "fa_wind_speed": ["high", "mid", "low", "stop"],
        "fa_work_mode": ["high", "mid", "low"],
        "fa_real_temp": True
    },

    "5-004-001": {
        "hp_set_temp_range": [5, 55],
        "hp_mode": ["cold", "hot"],
    },
    "5-004-002": {
        "hp_set_temp_range": [7, 55],
        "hp_mode": ["cold", "hot"],
        "hp_temp_adjust": ["up", "down"],
    },
    "5-004-003": {
    },
    "5-004-004": {
        "hp_set_temp_range": [5, 55],
        "hp_mode": ["cold", "hot"],
        "hp_temp_adjust": ["up", "down"],
    },
    "5-004-005": {
        "hp_set_temp_range": [7, 55],
        "hp_mode": ["cold", "hot"],
        "hp_hotwater_temp_adjust": ["up", "down"],
    },
    "5-004-006": {
        "hp_set_temp_range": [5, 55],
        "hp_mode": ["cold", "hot", "cold_common_hotwater", "cold_fast_hotwater", "hot_common_hotwater",
                    "hot_fast_hotwater", "common_hotwater", "fast_hotwater", "water_pump_loop"],
        "hp_temp_adjust": ["up", "down"],
    },
    "5-004-007": {
        "hp_set_temp_range": [12, 50],
        "hp_mode": ["cold", "hot"],
    },
    "5-004-008": {
        "hp_set_temp_range": [12, 55],
        "hp_mode": ["cold", "hot"],
    },
    "5-004-009": {
        "hp_set_temp_range": [5, 55],
        "hp_mode": ["cold", "hot"],
    },
    "5-004-010": {
        "hp_hot_set_temp": [30, 70],
        "hp_mode": ["cold", "hot"],
    },
    "5-005-001": {
        "tc_set_temp_range": [5, 35],
        "tc_lock_mode": ["mode", "mode_wind", "mode_wind_temp", "unlock"],
        "tc_mode": ["cold", "hot", "wet", "ventilate", "floorheat", "mix"],
        "tc_wind_speed": ["auto", "high", "mid_high", "mid", "mid_low", "low", "super_low"],
        "tc_temp_adjust": ["up", "down"],
        "tc_humidity_adjust": ["up", "down"],
        "tc_real_humidity": True,
        "tc_real_temp": True
    },
    "5-005-002": {
        "tc_set_temp_range": [5, 35],
        "tc_lock_mode": ["mode", "mode_wind", "mode_wind_temp", "child", "unlock"],
        "tc_mode": ["cold", "hot", "wet", "ventilate", "floorheat", "mix"],
        "tc_wind_speed": ["auto", "high", "mid", "low"],
        "tc_temp_adjust": ["up", "down"],
        "tc_humidity_adjust": ["up", "down"],
        "tc_real_humidity": True,
        "tc_real_temp": True
    },
    "5-005-003": {
        "tc_set_temp_range": [5, 35],
        "tc_lock_mode": ["unlock", "lock"],
        "tc_mode": ["cold", "hot", "ventilate", "floorheat", "mix"],
        "tc_wind_speed": ["auto", "high", "mid", "low"],
        "tc_temp_adjust": ["up", "down"],
        "tc_real_temp": True
    },
    "5-005-004": {
        "tc_set_temp_range": [5, 35],
        "tc_lock_mode": ["unlock", "lock"],
        "tc_mode": ["cold", "hot", "wet", "ventilate", "floorheat", "mix"],
        "tc_wind_speed": ["extreme_strong", "strong", "super_high", "high", "mid_high", "mid", "mid_low", "low",
                          "super_low", "extreme_low", "stop"],
        "tc_temp_adjust": ["up", "down"],
        "tc_real_temp": True
    },
    "5-005-005": {
        "tc_set_temp_range": [5, 35],
        "tc_mode": ["cold", "hot", "wet", "ventilate", "floorheat", "smart_floorheat"],
        "tc_wind_speed": ["auto", "high", "mid_high", "mid", "mid_low", "low", "super_low", "stop"],
        "tc_temp_adjust": ["up", "down"],
        "tc_real_temp": True
    },
    "5-005-006": {
        "tc_set_temp_range": [5, 35],
        "tc_mode": ["auto", "cold", "hot", "wet", "ventilate", "floorheat", "smart_floorheat"],
        "tc_wind_speed": ["auto", "high", "mid", "low"],
        "tc_temp_adjust": ["up", "down"],
        "tc_real_temp": True
    },
    "5-005-007": {
        "tc_set_temp_range": [5, 35],
        "tc_mode": ["auto", "cold", "hot", "wet", "ventilate", "floorheat", "smart_floorheat"],
        "tc_wind_speed": ["auto", "high", "mid", "low"],
        "tc_temp_adjust": ["up", "down"],
        "tc_real_temp": True
    },
    "5-005-008": {
        "tc_set_temp_range": [5, 35],
        "tc_mode": ["auto", "cold", "hot", "wet", "ventilate", "wet_reheat", "floorheat", "mix"],
        "tc_wind_speed": ["auto", "super_high", "high", "mid_high", "mid", "mid_low", "low", "super_low"],
        "tc_temp_adjust": ["up", "down"],
        "tc_real_temp": True
    },
    "5-005-009": {
        "tc_set_temp_range": [5, 35],
        "tc_mode": ["cold", "hot", "ventilate", "floorheat", "mix"],
        "tc_wind_speed": ["auto", "high", "mid", "low"],
        "tc_temp_adjust": ["up", "down"],
        "tc_real_temp": True
    },
    "5-005-010": {
        "tc_set_temp_range": [5, 35],
        "tc_mode": ["cold", "hot", "floorheat", "mix", "clean"],
        "tc_wind_speed": ["auto", "high", "mid", "low"],
        "tc_temp_adjust": ["up", "down"],
        "tc_real_temp": True
    },
    "5-005-011": {
        "tc_set_temp_range": [5, 35],
        "tc_mode": ["cold", "hot", "floorheat", "mix"],
        "tc_wind_speed": ["auto", "super_high", "high", "mid", "low", "super_low"],
        "tc_temp_adjust": ["up", "down"],
        "tc_real_temp": True
    },
    "5-005-012": {
        "tc_set_temp_range": [5, 35],
        "tc_mode": ["cold", "hot", "ventilate", "floorheat", "mix"],
        "tc_wind_speed": ["auto", "high", "mid", "low"],
        "tc_temp_adjust": ["up", "down"],
        "tc_real_temp": True
    },
    "5-005-013": {
        "tc_set_temp_range": [5, 35],
        "tc_mode": ["cold", "hot", "wet", "ventilate", "floorheat", "mix"],
        "tc_wind_speed": ["auto", "high", "mid", "low"],
        "tc_temp_adjust": ["up", "down"],
        "tc_real_humidity": True,
        "tc_real_temp": True
    },
    "5-005-014": {
        "tc_set_temp_range": [5, 35],
        "tc_mode": ["cold", "hot", "floorheat", "mix"],
        "tc_wind_speed": ["auto", "high", "mid", "low"],
        "tc_temp_adjust": ["up", "down"],
        "tc_real_temp": True
    },
    "5-005-015": {
        "tc_set_temp_range": [5, 35],
        "tc_mode": ["cold", "hot", "ventilate"],
    },
    "5-005-016": {
        "tc_set_temp_range": [5, 35],
        "tc_mode": ["cold", "hot", "wet", "ventilate", "floorheat", "mix"],
        "tc_wind_speed": ["auto", "high", "mid", "low"],
        "tc_real_temp": True
    },
    "5-005-017": {
        "tc_set_temp_range": [5, 35],
        "tc_mode": ["auto", "cold", "hot", "wet", "ventilate", "wet_reheat", "floorheat", "mix"],
        "tc_wind_speed": ["auto", "super_high", "high", "mid_high", "mid", "mid_low", "low", "super_low"],
        "tc_temp_adjust": ["up", "down"],
        "tc_real_temp": True
    },
}

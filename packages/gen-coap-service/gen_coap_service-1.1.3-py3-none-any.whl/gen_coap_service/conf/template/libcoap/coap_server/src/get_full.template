/* -*- Mode: C; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*-  */
/*
 * get_time.c
 * Copyright (C) 2020 coap_server Vladimir Roncevic <elektron.ronca@gmail.com>
 *
 * coap_server is free software: you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the
 * Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * coap_server is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 * See the GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along
 * with this program. If not, see <http://www.gnu.org/licenses/>.
 */

#include "server_api.h"

/**
 * Description:
 *     Getting current local time on host.
 *
 * Arguments:
 *     None
 *
 * Return value:
 *     Current local time from host in string format | NULL.
 */
char* get_time(void) {
    char *current_local_time = NULL;
    time_t host_time = time(NULL);
    struct tm *local_time = localtime(&host_time);
    if (local_time) {
        current_local_time = asctime(local_time);
    }
    return current_local_time;
}


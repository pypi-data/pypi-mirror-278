#
# Makefile.am
# Copyright (C) 2020 coap_client Vladimir Roncevic <elektron.ronca@gmail.com>
#
# coap_client is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# coap_client is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.
#

AM_LDFLAGS = -lcoap-1
AM_CPPFLAGS = -I/usr/include/coap/
AM_CXXFLAGS = -D_GNU_SOURCE -DWITH_POSIX
AM_CFLAGS = -D_GNU_SOURCE -DWITH_POSIX

bin_PROGRAMS = coap_client

coap_client_SOURCES = \
	main.c \
	print_usage.c \
	print_verbose.c \
	print_success.c \
	print_error.c \
	time_handler.c \
	client_api.h


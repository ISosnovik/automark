#!/bin/bash
# 
# AutoMark is a lightweight tool for testing programming assignments
#  
# Copyright (C) 2020 Ivan Sosnovik
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

mkdir -p ../automark_server/users/user_info
mkdir -p ../automark_server/users/user_progress
mkdir -p ../automark_server/assignments

# generate test_users
for i in {1..5}
do
    echo "{\"name\": \"user${i}\", \"mail\": \"test@mail.xyz\"}" > ../automark_server/users/user_info/id$i.json
done

# generate test assignments
python generate_assignments.py

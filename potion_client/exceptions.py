# Copyright 2014 Novo Nordisk Foundation Center for Biosustainability, DTU.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


class NotFoundException(Exception):
    pass


class BadRequestException(Exception):
    pass


class InternalServerErrorException(Exception):
    pass


HTTP_EXCEPTIONS = {
    400: BadRequestException("Bad Request (400)"),
    404: NotFoundException("Not Found (404)"),
    500: InternalServerErrorException("Internal Server Error (500)")
}
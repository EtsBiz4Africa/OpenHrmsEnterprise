# -*- coding: utf-8 -*-
######################################################################################
#
#    A part of Open HRMS Project <https://www.openhrms.com>
#
#    Copyright (C) 2022-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Cybrosys Techno Solutions (odoo@cybrosys.com)
#
#    This program is under the terms of the Odoo Proprietary License v1.0 (OPL-1)
#    It is forbidden to publish, distribute, sublicense, or sell copies of the Software
#    or modified copies of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#    DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
#    ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#    DEALINGS IN THE SOFTWARE.
#
########################################################################################

from odoo import tools
from odoo import models, fields, api, _


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    device_id = fields.Char(string='Biometric Device ID', help="Give the biometric device id")


class ZkMachine(models.Model):
    _name = 'zk.machine.attendance'
    _description = "ZKTeco Attendance"
    _inherit = 'hr.attendance'

    @api.constrains('check_in', 'check_out', 'employee_id')
    def _check_validity(self):
        """overriding the __check_validity function for employee attendance."""
        pass

    # device_id = fields.Char(string='Biometric Device ID', help="Biometric device id")
    device_id = fields.Many2one('zk.machine', string='Device ID', help="Address")
    punch_type = fields.Selection([('0', 'Check In'),
                                   ('1', 'Check Out'),
                                   ('2', 'Break Out'),
                                   ('3', 'Break In'),
                                   ('4', 'Overtime In'),
                                   ('5', 'Overtime Out')],
                                  string='Punching Type')

    attendance_type = fields.Selection([('1', 'Finger'),
                                        ('15', 'Face'),
                                        ('2', 'Type_2'),
                                        ('3', 'Password'),
                                        ('4', 'Card')], string='Category', help="Select the attendance type")
    punching_time = fields.Datetime(string='Punching Time', help="Give the punching time")
    address_id = fields.Many2one('res.partner', string='Working Address', help="Address")
    check_in = fields.Datetime(string="Check In", default=fields.Datetime.now, required=False)


class ReportZkDevice(models.Model):
    _name = 'zk.report.daily.attendance'
    _description = "Daily attendance"
    _auto = False
    _order = 'punching_day desc'

    name = fields.Many2one('hr.employee', string='Employee', help="Employee")
    punching_day = fields.Datetime(string='Date', help="Punching Date")
    address_id = fields.Many2one('res.partner', string='Working Address')
    attendance_type = fields.Selection([('1', 'Finger'),
                                        ('15', 'Face'),
                                        ('2', 'Type_2'),
                                        ('3', 'Password'),
                                        ('4', 'Card')],
                                       string='Category', help="Select the attendance type")
    punch_type = fields.Selection([('0', 'Check In'),
                                   ('1', 'Check Out'),
                                   ('2', 'Break Out'),
                                   ('3', 'Break In'),
                                   ('4', 'Overtime In'),
                                   ('5', 'Overtime Out')], string='Punching Type', help="Select the punch type")
    punching_time = fields.Datetime(string='Punching Time', help="Punching Time")
    check_in = fields.Datetime(string="Check In", required=False, )
    check_out = fields.Datetime(string="Check Out", required=False, )
    device_id = fields.Many2one('zk.machine', string='Device ID', help="Address")

    def init(self):
        tools.drop_view_if_exists(self._cr, 'zk_report_daily_attendance')
        query = """
            create or replace view zk_report_daily_attendance as (
                select
                    min(z.id) as id,
                    z.employee_id as name,
                    z.address_id as address_id,
                    z.check_in as punching_day,
                    z.attendance_type as attendance_type,
                    z.punching_time as punching_time,
                    z.punch_type as punch_type,
                    z.check_in as check_in,
                    z.check_out as check_out,
                    z.device_id as device_id
                from zk_machine_attendance z
                    join hr_employee e on (z.employee_id=e.id)
                    join zk_machine m on (z.device_id=m.id)
                GROUP BY
                    z.employee_id,
                    z.write_date,
                    z.address_id,
                    z.attendance_type,
                    z.punch_type,
                    z.punching_time,
                    z.check_out,
                    z.check_in,
                    z.device_id
            )
        """
        self._cr.execute(query)



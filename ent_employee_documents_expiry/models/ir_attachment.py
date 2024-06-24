# -*- coding: utf-8 -*-
################################################################################
#
#    A part of OpenHRMS Project <https://www.openhrms.com>
#
#    Copyright (C) 2024-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Cybrosys Techno Solutions (odoo@cybrosys.com)
#
#    This program is under the terms of the Odoo Proprietary License v1.0
#    (OPL-1)
#    It is forbidden to publish, distribute, sublicense, or sell copies of the
#    Software or modified copies of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#    DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#    OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE
#    USE OR OTHER DEALINGS IN THE SOFTWARE.
#
################################################################################
from odoo import fields, models


class IrAttachment(models.Model):
    """Add fields on the inherited model ir attachment"""
    _inherit = 'ir.attachment'

    doc_attach_rel_ids = fields.Many2many(comodel_name='hr.employee.document',
                                          relation='doc_attachment_ids',
                                          column1='attach_id3',
                                          column2='doc_id',
                                          string="Attachment",
                                          help="Attachment.")
    attach_rel_ids = fields.Many2many(comodel_name='hr.document',
                                      relation='attach_ids',
                                      column1='attachment_id3',
                                      column2='document_id',
                                      string="Attachment",
                                      help="Attachments.")
# -*- coding: utf-8 -*-
from plone import api
from collective.flexmailhost import log


def handler(obj, event):
    """Event handler to sync mail setting with MailHost"""
    mailhost = api.portal.get_tool("MailHost")
    log.info(
        "Handle IMailSchema IRecordEvent for field '{}' to update MailHost settings.".format(
            event.record.fieldName
        )
    )
    if event.record.fieldName == "smtp_host":
        mailhost.smtp_host = event.newValue
    if event.record.fieldName == "smtp_port":
        mailhost.smtp_port = event.newValue
    if event.record.fieldName == "smtp_userid":
        mailhost.smtp_uid = event.newValue
    if event.record.fieldName == "smtp_pass":
        mailhost.smtp_pwd = event.newValue

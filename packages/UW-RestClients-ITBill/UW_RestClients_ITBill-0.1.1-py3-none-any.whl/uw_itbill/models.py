# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from restclients_core import models
from uw_itbill.util import str_to_date, date_to_str, date_to_month
import json


class Subscription(models.Model):
    DRAFT = "draft"
    PROVISIONING = "provisioning"
    DEPLOYED = "deployed"
    DEPROVISION = "deprovision"
    CLOSED = "closed"
    CANCELLED = "cancelled"

    LIFECYCLE_CHOICES = (
        (DRAFT, "Draft"),
        (PROVISIONING, "Provisioning"),
        (DEPLOYED, "Deployed"),
        (DEPROVISION, "Deprovision"),
        (CLOSED, "Closed"),
        (CANCELLED, "Cancelled"),
    )

    sys_id = models.CharField(max_length=64)
    url = models.CharField(max_length=255, null=True)
    key_remote = models.CharField(max_length=127, null=True)
    name = models.CharField(max_length=255, null=True)
    lifecycle_state = models.CharField(
        max_length=32, choices=LIFECYCLE_CHOICES, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    note = models.CharField(max_length=255, null=True)
    work_notes = models.CharField(max_length=255, null=True)

    def __init__(self, *args, **kwargs):
        self.contact_number = {}
        self.product = {}
        self.contacts_additional = []
        self.budgets = []
        self.provisions = []

        data = kwargs.get("data")
        self.sys_id = data.get('sys_id')
        self.url = data.get('url')
        self.key_remote = data.get('key_remote')
        self.name = data.get('name')
        self.lifecycle_state = data.get('lifecycle_state')
        self.note = data.get('note')
        self.work_notes = data.get('work_notes')

        self.product = Product(data=data.get('product', {}))

        self.contact_number = Contact(data=data.get('contact_number', {}))
        for contact in data.get('contacts_additional', []):
            self.contacts_additional.append(contact)

        self.configuration_item = ConfigurationItem(
            data=data.get('configuration_item', {}))

        self.start_date = str_to_date(data.get('start_date'))
        self.end_date = str_to_date(data.get('end_date'))

        for budget in data.get('budgets', []):
            self.budgets.append(Budget(data=budget))

        for provision in data.get('provisions', []):
            self.provisions.append(
                Provision(data=provision.get('provision', {})))

    def json_data(self):
        return {
            "sys_id": self.sys_id,
            "url": self.url,
            "key_remote": self.key_remote,
            "name": self.name,
            "lifecycle_state": self.lifecycle_state,
            "product": self.product.json_data(),
            "note": self.note,
            "work_notes": self.work_notes,
            "contact_number": self.contact_number.json_data(),
            "contacts_additional": [
                c.json_data() for c in self.contacts_additional],
            "budgets": [
                b.json_data() for b in self.budgets],
            "provisions": [
                p.json_data() for p in self.provisions],
            "configuration_item": self.configuration_item.json_data(),
            "start_date": date_to_str(self.start_date),
            "end_date": date_to_str(self.end_date)
        }

    def __str__(self):
        return json.dumps(self.json_data())


class Product(models.Model):
    name = models.CharField(max_length=255, null=True)
    sys_id = models.CharField(max_length=64)
    url = models.CharField(max_length=255)

    def __init__(self, *args, **kwargs):
        data = kwargs.get('data')
        self.name = data.get('name')
        self.sys_id = data.get('sys_id')
        self.url = data.get('url')

    def json_data(self):
        return {
            "name": self.name,
            "sys_id": self.sys_id,
            "url": self.url
        }

    def __str__(self):
        return json.dumps(self.json_data())


class Budget(models.Model):
    ACTIVITY = "activity"
    COST_CENTER = "cost_center"
    GIFT = "gift"
    GRANT = "grant"
    PROGRAM = "program"
    PROJECT = "project"

    DRIVER_CHOICES = (
        (ACTIVITY, " Activity"),
        (COST_CENTER, "Cost Center"),
        (GIFT, "Gift"),
        (GRANT, "Grant"),
        (PROGRAM, "Program"),
        (PROJECT, "Project"),
    )

    sys_id = models.CharField(max_length=64)
    url = models.CharField(max_length=255)
    budget = models.CharField(max_length=32, null=True)
    budget_number = models.CharField(max_length=32, null=True)
    organization = models.CharField(max_length=255, null=True)
    pca_task = models.CharField(max_length=255, null=True)
    pca_option = models.CharField(max_length=255, null=True)
    pca_project = models.CharField(max_length=255, null=True)
    driver_worktag_type = models.CharField(
        max_length=16, choices=DRIVER_CHOICES)
    cost_center_driver = models.CharField(max_length=255, null=True)
    resource_driver = models.CharField(max_length=255, null=True)
    fund_driver = models.CharField(max_length=255, null=True)
    grant_adhoc = models.CharField(max_length=255, null=True)
    program_adhoc = models.CharField(max_length=255, null=True)
    gift_driver = models.CharField(max_length=255, null=True)
    grant_driver = models.CharField(max_length=255, null=True)
    cost_center_toggle = models.CharField(max_length=255, null=True)
    resource_toggle = models.CharField(max_length=255, null=True)
    program_driver = models.CharField(max_length=255, null=True)
    project_driver = models.CharField(max_length=255, null=True)
    activity_driver = models.CharField(max_length=255, null=True)
    activity = models.CharField(max_length=255, null=True)
    assignee = models.CharField(max_length=255, null=True)
    other_worktags = models.CharField(max_length=255, null=True)
    percent = models.SmallIntegerField(default=0)
    start_month = models.DateField()
    end_month = models.DateField(null=True)
    last_bill_end_period = models.CharField(max_length=255, null=True)
    stage = models.CharField(max_length=64, null=True)

    def __init__(self, *args, **kwargs):
        data = kwargs.get('data')
        self.sys_id = data.get('sys_id')
        self.url = data.get('url')
        self.budget = data.get('budget')
        self.budget_number = data.get('budget_number')
        self.organization = data.get('organization')
        self.pca_task = data.get('pca_task')
        self.pca_option = data.get('pca_option')
        self.pca_project = data.get('pca_project')
        self.driver_worktag_type = data.get('driver_worktag_type')
        self.cost_center_driver = data.get('cost_center_driver')
        self.resource_driver = data.get('resource_driver')
        self.fund_driver = data.get('fund_driver')
        self.grant_adhoc = data.get('grant_adhoc')
        self.program_adhoc = data.get('program_adhoc')
        self.gift_driver = data.get('gift_driver')
        self.grant_driver = data.get('grant_driver')
        self.cost_center_toggle = data.get('cost_center_toggle')
        self.resource_toggle = data.get('resource_toggle')
        self.program_driver = data.get('program_driver')
        self.project_driver = data.get('project_driver')
        self.activity_driver = data.get('activity_driver')
        self.activity = data.get('activity')
        self.assignee = data.get('assignee')
        self.other_worktags = data.get('other_worktags')
        self.percent = data.get('percent')
        self.start_month = str_to_date(data.get('start_month'))
        self.end_month = str_to_date(data.get('end_month'))
        self.last_bill_end_period = data.get('last_bill_end_period')
        self.stage = data.get('stage')

    def json_data(self):
        return {
            "sys_id": self.sys_id,
            "url": self.url,
            "budget": self.budget,
            "budget_number": self.budget_number,
            "organization": self.organization,
            "pca_task": self.pca_task,
            "pca_option": self.pca_option,
            "pca_project": self.pca_project,
            "driver_worktag_type": self.driver_worktag_type,
            "cost_center_driver": self.cost_center_driver,
            "resource_driver": self.resource_driver,
            "fund_driver": self.fund_driver,
            "grant_adhoc": self.grant_adhoc,
            "program_adhoc": self.program_adhoc,
            "gift_driver": self.gift_driver,
            "grant_driver": self.grant_driver,
            "cost_center_toggle": self.cost_center_toggle,
            "resource_toggle": self.resource_toggle,
            "program_driver": self.program_driver,
            "project_driver": self.project_driver,
            "activity_driver": self.activity_driver,
            "activity": self.activity,
            "assignee": self.assignee,
            "other_worktags": self.other_worktags,
            "percent": self.percent,
            "start_month": date_to_month(self.start_month),
            "end_month": date_to_month(self.end_month),
            "last_bill_end_period": self.last_bill_end_period,
            "stage": self.stage
        }


class Provision(models.Model):
    ANNUAL = "annual"
    ANNUAL_FIXED = "annual-fixed"
    MONTHLY = "monthly"
    MONTHLY_METERED = "monthly-metered"
    ONETIME = "onetime"
    QUARTER_FISCAL = "quarter-fiscal"

    BILL_SCHEDULE_CHOICES = (
        (ANNUAL, "Annual"),
        (ANNUAL_FIXED, "Annual-Fixed"),
        (MONTHLY, "Monthly"),
        (MONTHLY_METERED, "Monthly-Metered"),
        (ONETIME, "Onetime"),
        (QUARTER_FISCAL, "Quarter-Fiscal"),
    )

    sys_id = models.CharField(max_length=64)
    name = models.CharField(max_length=255)
    bill_schedule = models.CharField(
        max_length=16, choices=BILL_SCHEDULE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    last_bill_end_period = models.DateField(null=True)
    next_bill_start = models.DateField(null=True)
    stage = models.CharField(max_length=64, null=True)
    note = models.CharField(max_length=255)
    key_remote = models.CharField(max_length=127, null=True)
    current_quantity = models.SmallIntegerField(default=0)

    def __init__(self, *args, **kwargs):
        self.product = {}
        self.subscription = {}
        self.quantities = []
        self.budgets = []

        data = kwargs.get("data")
        self.sys_id = data.get('sys_id')
        self.name = data.get('name')
        self.product = Product(data=data.get('product'))
        self.subscription = Subscription(data=data.get('subscription'))
        self.bill_schedule = data.get('bill_schedule')
        self.start_date = str_to_date(
            data.get('start_date'))
        self.end_date = str_to_date(
            data.get('end_date'))
        self.last_bill_end_period = str_to_date(
            data.get('last_bill_end_period'))
        self.next_bill_start = str_to_date(
            data.get('next_bill_start'))
        self.stage = data.get('stage')
        self.note = data.get('note')
        self.key_remote = data.get('key_remote')
        self.current_quantity = float(data.get('current_quantity', 0))
        for quantity in data.get('quantities', []):
            self.quantities.append(Quantity(data=quantity))
        for budget in data.get('budgets', []):
            self.budgets.append(Budget(data=budget))

    def json_data(self):
        return {
            "sys_id": self.sys_id,
            "name": self.name,
            "bill_schedule": self.bill_schedule,
            "start_date": date_to_str(self.start_date),
            "end_date": date_to_str(self.end_date),
            "last_bill_end_period": date_to_str(self.last_bill_end_period),
            "next_bill_start": date_to_str(self.next_bill_start),
            "stage": self.stage,
            "note": self.note,
            "key_remote": self.key_remote,
            "current_quantity": self.current_quantity,
            "product": self.product.json_data(),
            "subscription": self.subscription.json_data(),
            "quantities": [
                q.json_data() for q in self.quantities],
            "budgets": [
                b.json_data() for b in self.budgets],
        }

    def __str__(self):
        return json.dumps(self.json_data())


class Quantity(models.Model):
    sys_id = models.CharField(max_length=64)
    url = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    last_bill_end_period = models.DateField(null=True)
    next_bill_start = models.DateField(null=True)
    stage = models.CharField(max_length=64, null=True)
    quantity = models.FloatField()
    bill_comment = models.CharField(max_length=255)

    def __init__(self, *args, **kwargs):
        data = kwargs.get('data')
        self.sys_id = data.get('sys_id')
        self.url = data.get('url')
        self.start_date = str_to_date(
            data.get('start_date'))
        self.end_date = str_to_date(
            data.get('end_date'))
        self.last_bill_end_period = str_to_date(
            data.get('last_bill_end_period'))
        self.next_bill_start = str_to_date(
            data.get('next_bill_start'))
        self.stage = data.get('stage')
        self.quantity = float(data.get('quantity', 0))
        self.bill_comment = data.get('bill_comment')

    def json_data(self):
        return {
            "sys_id": self.sys_id,
            "url": self.url,
            "start_date": date_to_str(self.start_date),
            "end_date": date_to_str(self.end_date),
            "last_bill_end_period": date_to_str(self.last_bill_end_period),
            "next_bill_start": date_to_str(self.next_bill_start),
            "stage": self.stage,
            "quantity": self.quantity,
            "bill_comment": self.bill_comment,
        }

    def __str__(self):
        return json.dumps(self.json_data())


class ConfigurationItem(models.Model):
    name = models.CharField(max_length=255)
    sys_id = models.CharField(max_length=64)
    url = models.CharField(max_length=255)

    def __init__(self, *args, **kwargs):
        data = kwargs.get('data')
        self.name = data.get('name')
        self.sys_id = data.get('sys_id')
        self.url = data.get('url')

    def json_data(self):
        return {
            "name": self.name,
            "sys_id": self.sys_id,
            "url": self.url
        }

    def __str__(self):
        return json.dumps(self.json_data())


class Contact(models.Model):
    number = models.CharField(max_length=32)

    def __init__(self, *args, **kwargs):
        data = kwargs.get('data')
        self.number = data.get('number')

    def json_data(self):
        return {
            "number": self.number
        }

    def __str__(self):
        return json.dumps(self.json_data())

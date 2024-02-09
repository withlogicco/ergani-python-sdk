from dataclasses import dataclass, field
from datetime import date, datetime, time
from typing import List, Literal, Optional, TypedDict

from ergani.typings import (
    LateDeclarationJustificationType,
    OvertimeJustificationType,
    ScheduleWorkType,
    WorkCardMovementType,
)
from ergani.utils import (
    format_date,
    format_datetime,
    format_time,
    get_day_of_week,
    get_ergani_late_declaration_justification,
    get_ergani_overtime_cancellation,
    get_ergani_overtime_justification,
    get_ergani_work_type,
    get_ergani_workcard_movement_type,
)


@dataclass
class WorkCard:
    """
    Represents a work card entry for an employee

    Attributes:
        employee_tax_identification_number (str): The employee's tax identification number
        employee_last_name (str): The last name of the employee
        employee_first_name (str): The first name of the employee
        work_card_movement_type (WorkCardMovementType): The type of work card movement
        work_card_submission_date (date): The date the work card was submitted
        work_card_movement_datetime (datetime): The exact date and time of the work card movement
        late_declaration_justification (Optional[LateDeclarationJustificationType]): The justification for the late declaration of the work card movement
    """

    employee_tax_identification_number: str
    employee_last_name: str
    employee_first_name: str
    work_card_movement_type: WorkCardMovementType
    work_card_submission_date: date
    work_card_movement_datetime: datetime
    late_declaration_justification: Optional[LateDeclarationJustificationType] = None

    def serialize(self):
        return {
            "f_afm": self.employee_tax_identification_number,
            "f_eponymo": self.employee_last_name,
            "f_onoma": self.employee_first_name,
            "f_type": get_ergani_workcard_movement_type(self.work_card_movement_type),
            "f_reference_date": self.work_card_submission_date.isoformat(),
            "f_date": format_datetime(self.work_card_movement_datetime),
            "f_aitiologia": get_ergani_late_declaration_justification(
                self.late_declaration_justification
            ),
        }


@dataclass
class CompanyWorkCard:
    """
    Represents work card entries that are issued on a single business branch

    Attributes:
        employer_tax_identification_number (str): The employer's tax identification number
        business_branch_number (int): The number identifying the specific business branch
        comments (Optional[str]): Additional comments related to the work cards
        card_details (List[WorkCard]): A list of `WorkCard` entries for the business branch
    """

    employer_tax_identification_number: str
    business_branch_number: int
    comments: Optional[str] = ""
    card_details: List[WorkCard] = field(default_factory=list)

    def serialize(self):
        return {
            "f_afm_ergodoti": self.employer_tax_identification_number,
            "f_aa": self.business_branch_number,
            "f_comments": self.comments,
            "Details": {
                "CardDetails": [
                    work_card.serialize() for work_card in self.card_details
                ]
            },
        }


@dataclass
class Overtime:
    """
    Represents an overtime entry for an employee

    Attributes:
        employee_tax_identification_number (str): The employee's tax identification number
        employee_social_security_number (str): The employee's social security number
        employee_last_name (str): The last name of the employee
        employee_first_name (str): The first name of the employee
        overtime_date (date): The date of the overtime
        overtime_start_time (time): The start time of the overtime period
        overtime_end_time (time): The end time of the overtime period
        overtime_cancellation (bool): Indicates if the overtime was cancelled or not
        employee_profession_code (str): The profession code of the employee
        overtime_justification (OvertimeJustificationType): The justification for the overtime
        weekly_workdays_number (Literal[5, 6]): The number of the employee's working days in a week
        asee_approval (Optional[str]): The ASEE aproval
    """

    employee_tax_identification_number: str
    employee_social_security_number: str
    employee_last_name: str
    employee_first_name: str
    overtime_date: date
    overtime_start_time: time
    overtime_end_time: time
    overtime_cancellation: bool
    employee_profession_code: str
    overtime_justification: OvertimeJustificationType
    weekly_workdays_number: Literal[5, 6]
    asee_approval: Optional[str] = ""

    def serialize(self):
        return {
            "f_afm": self.employee_tax_identification_number,
            "f_amka": self.employee_social_security_number,
            "f_eponymo": self.employee_last_name,
            "f_onoma": self.employee_first_name,
            "f_date": format_date(self.overtime_date),
            "f_from": format_time(self.overtime_start_time),
            "f_to": format_time(self.overtime_end_time),
            "f_cancellation": get_ergani_overtime_cancellation(
                self.overtime_cancellation
            ),
            "f_step": self.employee_profession_code,
            "f_reason": get_ergani_overtime_justification(self.overtime_justification),
            "f_weekdates": self.weekly_workdays_number,
            "f_asee": self.asee_approval,
        }


@dataclass
class CompanyOvertime:
    """
    Represents overtime entries that are issued on a single business branch

    Attributes:
        business_branch_number (int): The number identifying the specific business branch
        sepe_service_code (str): The SEPE service code
        business_primary_activity_code (str): The primary activity code of the business
        business_branch_activity_code (str): The activity code for the specific branch
        kallikratis_municipal_code (str): The kallikratis municipal code
        legal_representative_tax_identification_number (str): Tax identification number of the legal representative
        employee_overtimes (List[Overtime]): A list of `Overtime` entries for employees
        related_protocol_id (Optional[str]): Related protocol ID
        related_protocol_date (Optional[date]): The date of the related protocol
        employer_organization (Optional[str]): The employer's organization name
        business_secondary_activity_code_1 (Optional[str]): Secondary activity code 1
        business_secondary_activity_code_2 (Optional[str]): Secondary activity code 2
        business_secondary_activity_code_3 (Optional[str]): Secondary activity code 3
        business_secondary_activity_code_4 (Optional[str]): Secondary activity code 4
        comments (Optional[str]): Additional comments related to the overtime entries
    """

    business_branch_number: int
    sepe_service_code: str
    business_primary_activity_code: str
    business_branch_activity_code: str
    kallikratis_municipal_code: str
    legal_representative_tax_identification_number: str
    employee_overtimes: List[Overtime] = field(default_factory=list)
    related_protocol_id: Optional[str] = ""
    related_protocol_date: Optional[date] = None
    employer_organization: Optional[str] = ""
    business_secondary_activity_code_1: Optional[str] = ""
    business_secondary_activity_code_2: Optional[str] = ""
    business_secondary_activity_code_3: Optional[str] = ""
    business_secondary_activity_code_4: Optional[str] = ""
    comments: Optional[str] = ""

    def serialize(self):
        return {
            "f_aa_pararthmatos": self.business_branch_number,
            "f_rel_protocol": self.related_protocol_id,
            "f_rel_date": format_date(self.related_protocol_date),
            "f_ypiresia_sepe": self.sepe_service_code,
            "f_ergodotikh_organwsh": self.employer_organization,
            "f_kad_kyria": self.business_primary_activity_code,
            "f_kad_deyt_1": self.business_secondary_activity_code_1,
            "f_kad_deyt_2": self.business_secondary_activity_code_2,
            "f_kad_deyt_3": self.business_secondary_activity_code_3,
            "f_kad_deyt_4": self.business_secondary_activity_code_4,
            "f_kad_pararthmatos": self.business_branch_activity_code,
            "f_kallikratis_pararthmatos": self.kallikratis_municipal_code,
            "f_comments": self.comments,
            "f_afm_proswpoy": self.legal_representative_tax_identification_number,
            "Ergazomenoi": {
                "OvertimeErgazomenosDate": [
                    overtime.serialize() for overtime in self.employee_overtimes
                ]
            },
        }


@dataclass
class WorkdayDetails:
    """
    Represents details of an employee's workday

    Attributes:
        work_type (ScheduleWorkType): The type of an employee's work schedule
        start_time (time): The start time of the workday
        end_time (time): The end time of the workday
    """

    work_type: ScheduleWorkType
    start_time: time
    end_time: time

    def serialize(self):
        return {
            "f_type": get_ergani_work_type(self.work_type),
            "f_from": format_time(self.start_time),
            "f_to": format_time(self.end_time),
        }


@dataclass
class EmployeeDailySchedule:
    """
    Represents a daily schedule entry for an employee

    Attributes:
        employee_tax_identification_number (str): The employee's tax identification number
        employee_last_name (str): The employee's last name
        employee_first_name (str): The employee's first name
        schedule_date (date): The date of the schedule
        workday_details (List[WorkdayDetails]): A list of workday detail entries for the employee
    """

    employee_tax_identification_number: str
    employee_last_name: str
    employee_first_name: str
    schedule_date: date
    workday_details: List[WorkdayDetails] = field(default_factory=list)

    def serialize(self):
        return {
            "f_afm": self.employee_tax_identification_number,
            "f_eponymo": self.employee_last_name,
            "f_onoma": self.employee_first_name,
            "f_date": format_date(self.schedule_date),
            "ErgazomenosAnalytics": {
                "ErgazomenosWTOAnalytics": [
                    workday_detail.serialize()
                    for workday_detail in self.workday_details
                ]
            },
        }


@dataclass
class CompanyDailySchedule:
    """
    Represents daily schedule entries that are issued on a single business branch

    Attributes:
        business_branch_number (int): The number identifying the business branch
        start_date (Optional[date]): The start date of the schedule
        end_date (Optional[date]): The end date of the schedule period
        employee_schedules (List[EmployeeDailySchedule]): A list of daily schedules for employees
        related_protocol_id (Optional[str]): The ID of the related protocol
        related_protocol_date (Optional[date]): The date of the related protocol
        comments (Optional[str]): Additional comments regarding the daily schedule entries
    """

    business_branch_number: int
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    employee_schedules: List[EmployeeDailySchedule] = field(default_factory=list)
    related_protocol_id: Optional[str] = ""
    related_protocol_date: Optional[date] = None
    comments: Optional[str] = ""

    def serialize(self):
        return {
            "f_aa_pararthmatos": self.business_branch_number,
            "f_rel_protocol": self.related_protocol_id,
            "f_rel_date": format_date(self.related_protocol_date),
            "f_comments": self.comments,
            "f_from_date": format_date(self.start_date),
            "f_to_date": format_date(self.end_date),
            "Ergazomenoi": {
                "ErgazomenoiWTO": [
                    employee_schedule.serialize()
                    for employee_schedule in self.employee_schedules
                ]
            },
        }


@dataclass
class EmployeeWeeklySchedule:
    """
    Represents a weekly schedule entry for an employee

    Attributes:
        employee_tax_identification_number (str): The employee's tax identification number
        employee_last_name (str): The employee's last name
        employee_first_name (str): The employee's first name
        schedule_date (date): The date of the schedule
        workday_details (List[WorkdayDetails]): A list of workday detail entries for the week
    """

    employee_tax_identification_number: str
    employee_last_name: str
    employee_first_name: str
    schedule_date: date
    workday_details: List[WorkdayDetails] = field(default_factory=list)

    def serialize(self):
        return {
            "f_afm": self.employee_tax_identification_number,
            "f_eponymo": self.employee_last_name,
            "f_onoma": self.employee_first_name,
            "f_day": get_day_of_week(self.schedule_date),
            "ErgazomenosAnalytics": {
                "ErgazomenosWTOAnalytics": [
                    workday_detail.serialize()
                    for workday_detail in self.workday_details
                ]
            },
        }


@dataclass
class CompanyWeeklySchedule:
    """
    Represents weekly schedule entries that are issued on a single business branch

    Attributes:
        business_branch_number (int): The number identifying the business branch
        start_date (date): The start date of the weekly schedule
        end_date (date): The end date of the weekly schedule
        employee_schedules (List[EmployeeWeeklySchedule]): A list of weekly schedules for employees
        related_protocol_id (Optional[str]): The ID of the related protocol
        related_protocol_date (Optional[date]): The date of the related protocol
        comments (Optional[str]): Additional comments regarding the weekly schedule entries
    """

    business_branch_number: int
    start_date: date
    end_date: date
    employee_schedules: List[EmployeeWeeklySchedule] = field(default_factory=list)
    related_protocol_id: Optional[str] = ""
    related_protocol_date: Optional[date] = None
    comments: Optional[str] = ""

    def serialize(self):
        return {
            "f_aa_pararthmatos": self.business_branch_number,
            "f_rel_protocol": self.related_protocol_id,
            "f_rel_date": format_date(self.related_protocol_date),
            "f_comments": self.comments,
            "f_from_date": format_date(self.start_date),
            "f_to_date": format_date(self.end_date),
            "Ergazomenoi": {
                "ErgazomenoiWTO": [
                    employee_schedule.serialize()
                    for employee_schedule in self.employee_schedules
                ]
            },
        }

    class SubmissionResponse(TypedDict):
        """
        Represents a submission response from the Ergani API

        Attributes:
            submission_id (str): The unique identifier of the submission
            protocol (str): The protocol associated with the submission
            submission_date (datetime): The datetime of the submission
        """

        submission_id: str
        protocol: str
        submission_date: datetime

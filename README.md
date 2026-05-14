# Ergani Python SDK

`ergani` is a Python SDK for interacting with the API of [Ergani](https://www.gov.gr/en/ipiresies/ergasia-kai-asphalise/apozemioseis-kai-parokhes/prosopopoiemene-plerophorese-misthotou-ergane).

> [!TIP]
> ## 🌟 Production ready 🌟
>
> The Ergani Python SDK is battle-tested for production in:
>
> - **JobCard** (https://jobcard.gr): Turnkey self-service solution for the digital work card time attendance tracking and digital scheduling
> - **Digital work card solutions with LOGIC** (https://withlogic.co/solutions/digital-work-card): Custom digital work card solutions, tailor-made for the most demanding businesses.

## Requirements

Python 3.10 or later


## Installation
The `ergani` package is available on PyPI and you can install it through your favorite package manager:

```bash
pip install ergani
```

## Usage

### Create a client

To create a new Ergani client you have to set your Ergani username, password and optionally the Ergani API base URL, that defaults to https://trialeservices.yeka.gr/WebServicesAPI/api.

```py
import os
from ergani.client import ErganiClient

ERGANI_USERNAME = os.environ.get("ERGANI_USERNAME", "")
ERGANI_PASSWORD = os.environ.get("ERGANI_PASSWORD", "")
ERGANI_BASE_URL = os.environ.get("ERGANI_BASE_URL", "")

ergani_client = ErganiClient(ERGANI_USERNAME, ERGANI_PASSWORD)
```

If you intend to use this package for multiple company entities, it is necessary to create separate client instances for each entity with the appropriate credentials.

We are going to use the aforementioned `ergani_client` for the following usage examples.

### Work card

Submit work card records to Ergani in order to declare an employee's movement (arrival, departure).

```py
def submit_work_card(company_work_cards: List[CompanyWorkCard]) -> (Response | None)
```

#### Example

```py
from datetime import datetime, timedelta
from ergani.models import CompanyWorkCard, WorkCard

today = datetime.today()
yesterday = today - timedelta(days=1)

work_card_1 = WorkCard(
    employee_tax_identification_number="123456789",
    employee_first_name="first_name",
    employee_last_name="last_name",
    work_card_movement_type="ARRIVAL",
    work_card_submission_date=today.date(),
    work_card_movement_datetime=today,
)

work_card_2 = WorkCard(
    employee_tax_identification_number="123456789",
    employee_first_name="first_name",
    employee_last_name="last_name",
    work_card_movement_type="ARRIVAL",
    work_card_submission_date=today.date(),
    work_card_movement_datetime=today,
)

company_work_card_1 = CompanyWorkCard(
    employer_tax_identification_number="123456789",
    business_branch_number=1,
    card_details=[work_card_1, work_card_2],
)

work_card_3 = WorkCard(
    employee_tax_identification_number="123456789",
    employee_first_name="first_name",
    employee_last_name="last_name",
    work_card_movement_type="ARRIVAL",
    work_card_submission_date=today.date(),
    work_card_movement_datetime=yesterday,
    late_declaration_justification="POWER_OUTAGE",
)

company_work_card_2 = CompanyWorkCard(
    employer_tax_identification_number="123456789",
    business_branch_number=2,
    card_details=[work_card_3],
)

company_work_cards = [company_work_card_1, company_work_card_2]
response = ergani_client.submit_work_card(company_work_cards=company_work_cards)
```

**Note:** You can submit work cards for various employees across multiple company branches simultaneously as shown above.

### Overtime

Submit overtime records to Ergani in order to declare employees overtimes.

```py
def submit_overtime(company_overtimes: List[CompanyOvertime]) -> (Response | None)
```

#### Example

```py
from datime import datetime
from ergani.models import CompanyOvertime, Overtime

today = datetime.today()

overtime = Overtime(
    employee_tax_identification_number="123456789",
    employee_social_security_number="123456789",
    employee_first_name="first_name",
    employee_last_name="last_name",
    overtime_date=today.date(),
    overtime_start_time=time(hour=18),
    overtime_end_time=time(hour=20),
    overtime_cancellation=False,
    employee_profession_code="123456",
    overtime_justification="EXCEPTIONAL_WORKLOAD",
    weekly_workdays_number=5,
)

company_overtime = CompanyOvertime(
    business_branch_number=1,
    sepe_service_code="12345",
    business_primary_activity_code="1234",
    business_branch_activity_code="1234",
    kallikratis_municipal_code="12345678",
    legal_representative_tax_identification_number="123456789",
    employee_overtimes=[overtime],
)

company_overtimes = [company_overtime]
response = ergani_client.submit_overtime(company_overtimes=company_overtimes)
```

**Note:** You can submit overtime records for various employees across multiple company branches simultaneously.

### Daily schedule

Submit daily schedules to Ergani in order to declare schedules for employees that don't have a fixed schedule (e.g. shift workers).

```py
def submit_daily_schedule(company_daily_schedules: List[CompanyDailySchedule]) -> (Response | None)
```

#### Example

```py
from datime import datetime, timedelta
from ergani.models import CompanyDailySchedule, EmployeeDailySchedule, WorkdayDetails

today = datetime.today()
tomorrow = today + timedelta(days=1)

workday_details = WorkdayDetails(
    work_type="WORK_FROM_HOME", start_time=time(hour=9), end_time=time(hour=17)
)

employee_daily_schedule = EmployeeDailySchedule(
    employee_tax_identification_number="123456789",
    employee_first_name="first_name",
    employee_last_name="last_name",
    schedule_date=tomorrow.date(),
    workday_details=[workday_details],
)

company_daily_schedule = CompanyDailySchedule(
    business_branch_number=1, employee_schedules=[employee_daily_schedule]
)

company_daily_schedules = [company_daily_schedule]
response = ergani_client.submit_daily_schedule(
    company_daily_schedules=company_daily_schedules
)
```

### Weekly schedule

Submit weekly schedules to Ergani in order to declare schedules for employees that have a fixed schedule.

```py
def submit_weekly_schedule(company_weekly_schedules: List[CompanyWeeklySchedule]) -> (Response | None)
```

#### Example

```py
from datime import datetime, timedelta
from ergani.models import CompanyDailySchedule, EmployeeDailySchedule, WorkdayDetails

today = datetime.today()
days_until_next_monday = (0 - today.weekday() + 7) % 7
next_week_monday = today + timedelta(days=days_until_next_monday)

next_week_start = next_week_monday.replace(hour=0, minute=0, second=0, microsecond=0)
next_week_end = next_week_start + timedelta(days=5)

workday_details = WorkdayDetails(
    work_type="WORK_FROM_HOME", start_time=time(hour=9), end_time=time(hour=17)
)

employee_weekly_schedule = []

for i in range(5):  # 5 days in a work week (Monday to Friday)
    current_day = next_week_start + timedelta(days=i)

    schedule = EmployeeWeeklySchedule(
        employee_tax_identification_number="123456789",
        employee_first_name="first_name",
        employee_last_name="last_name",
        schedule_date=current_day.date(),
        workday_details=[workday_details],
    )

    employee_weekly_schedule.append(schedule)

company_weekly_schedule = CompanyWeeklySchedule(
    business_branch_number=1,
    employee_schedules=[employee_weekly_schedule],
    start_date=next_week_start,
    end_date=next_week_end,
)

company_weekly_schedules = [company_weekly_schedule]
response = ergani_client.submit_weekly_schedule(
    company_weekly_schedules=company_weekly_schedules
)
```

**Note:** You can submit weekly schedules for various employees across multiple company branches simultaneously.

### Monthly status

Fetch monthly status records from the ``EX_BASE_04`` ExecuteService endpoint for a specific reporting period.

```py
records = ergani_client.get_monthly_status(report_year=2026, report_month=4)

for record in records:
    print(record.raw_payload)
```

``MonthlyStatusRecord`` intentionally exposes the raw payload because the trial environment's service metadata documents the request fields but not a stable response schema.

---

Full reference documentation is available at [https://ergani.withlogic.dev/](https://ergani.withlogic.dev/).

## Glossary

The glossary might help you if you're taking a look at the official documentation of the Ergani API (https://eservices.yeka.gr/(S(ayldvlj35eukgvmzrr055oe5))/Announcements.aspx?id=257).


### Work card

| **Original**       | **Original help text** (in Greek)                         | **Translated**                                |
|--------------------|-----------------------------------------------------------|-----------------------------------------------|
| `f_afm_ergodoti`   | Α.Φ.Μ Εργοδότη (Για επαλήθευση)                           | `employer_tax_identification_number`          |
| `f_aa`             | Α/Α Παραρτήματος                                          | `business_branch_number`                      |
| `f_comments`       | ΣΧΟΛΙΑ                                                    | `comments`                                    |
| `f_afm`            | ΑΡΙΘΜΟΣ ΦΟΡΟΛΟΓΙΚΟΥ ΜΗΤΡΩΟΥ (Α.Φ.Μ.)                      | `employee_tax_indentification_number`         |
| `f_eponymo`        | ΕΠΩΝΥΜΟ                                                   | `employee_last_name`                          |
| `f_onoma`          | ΟΝΟΜΑ                                                     | `employee_first_name`                         |
| `f_type`           | Τύπος Κίνησης                                             | `work_card_movement_type`                     |
| `f_reference_date` | ΗΜ/ΝΙΑ Αναφοράς                                           | `work_card_submission_date`                   |
| `f_date`           | ΗΜ/ΝΙΑ Κίνησης                                            | `work_card_movement_datetime`                 |
| `f_aitiologia`     | ΚΩΔΙΚΟΣ ΑΙΤΙΟΛΟΓΙΑΣ (Σε περίπτωση Εκπρόθεσμου)            | `late_declaration_justification`              |

#### Work card movement types

| **Original API code**   | **Original help text** (in Greek) | **Translated** |
|-------------------------|-----------------------------------|----------------|
| `0`                     | ΠΡΟΣΕΛΕΥΣΗ                        | `ARRIVAL`      |
| `1`                     | ΑΠΟΧΩΡΗΣΗ                         | `DEPARTURE`    |

#### Work card justifications

| **Original API code**   | **Original help text** (in Greek)                        | **Translated**                 |
|-------------------------|----------------------------------------------------------|--------------------------------|
| `001`                   | ΠΡΟΒΛΗΜΑ ΣΤΗΝ ΗΛΕΚΤΡΟΔΟΤΗΣΗ/ΤΗΛΕΠΙΚΟΙΝΩΝΙΕΣ              | `POWER_OUTAGE`                 |
| `002`                   | ΠΡΟΒΛΗΜΑ ΣΤΑ ΣΥΣΤΗΜΑΤΑ ΤΟΥ ΕΡΓΟΔΟΤΗ                      | `EMPLOYER_SYSTEMS_UNAVAILABLE` |
| `003`                   | ΠΡΟΒΛΗΜΑ ΣΥΝΔΕΣΗΣ ΜΕ ΤΟ ΠΣ ΕΡΓΑΝΗ                        | `ERGANI_SYSTEMS_UNAVAILABLE`   |

### Overtime

| **Original**                 | **Original help text** (in Greek)                            | **Translated**                                  |
|------------------------------|--------------------------------------------------------------|-------------------------------------------------|
| `f_aa`                       | Α/Α Παραρτήματος                                             | `business_branch_number`                        |
| `f_rel_protocol`             | ΣΧΕΤΙΚΟ ΕΝΤΥΠΟ ΑΡΙΘ. ΠΡΩΤ.	                                  | `related_protocol_id`                           |
| `f_rel_date`                 | ΣΧΕΤΙΚΟ ΕΝΤΥΠΟ ΗΜΕΡΟΜΗΝΙΑ	                                  | `related_protocol_date`                         |
| `f_ypiresia_sepe`            | ΚΩΔΙΚΟΣ ΥΠΗΡΕΣΙΑΣ ΣΕΠΕ	                                      | `sepe_service_code`                             |
| `f_ergodotikh_organwsh`      | ΕΡΓΟΔΟΤΙΚΗ ΟΡΓΑΝΩΣΗ	                                        | `employer_organization`                         |
| `f_kad_kyria`                | Κ.Α.Δ. - ΚΥΡΙΑ ΔΡΑΣΤΗΡΙΟΤΗΤΑ	                                | `business_primary_activity_code`                |
| `f_kad_deyt_1`               | Κ.Α.Δ. - ΚΥΡΙΑ ΔΡΑΣΤΗΡΙΟΤΗΤΑ	1                               | `business_secondary_activity_code_1`            |
| `f_kad_deyt_2`               | Κ.Α.Δ. - ΚΥΡΙΑ ΔΡΑΣΤΗΡΙΟΤΗΤΑ	2                               | `business_secondary_activity_code_2`            |
| `f_kad_deyt_3`               | Κ.Α.Δ. - ΚΥΡΙΑ ΔΡΑΣΤΗΡΙΟΤΗΤΑ	3                               | `business_secondary_activity_code_3`            |
| `f_kad_deyt_4`               | Κ.Α.Δ. - ΚΥΡΙΑ ΔΡΑΣΤΗΡΙΟΤΗΤΑ	4                               | `business_secondary_activity_code_4`            |
| `f_kad_pararthmatos`         | Κ.Α.Δ. ΠΑΡΑΡΤΗΜΑΤΟΣ	                                        | `business_brach_activity_code`                  |
| `f_kallikratis_pararthmatos` | ΔΗΜΟΤΙΚΗ / ΤΟΠΙΚΗ ΚΟΙΝΟΤΗΤΑ	                                | `kallikratis_municipal_code`                    |
| `f_comments`                 | ΠΑΡΑΤΗΡΗΣΕΙΣ                                                 | `comments`                                      |
| `f_afm_proswpoy`             | Νόμιμος Εκπρόσωπος(Α.Φ.Μ.)                                   | `legal_representative_tax_identification_number`|
| `f_afm`                      | ΑΡΙΘΜΟΣ ΦΟΡΟΛΟΓΙΚΟΥ ΜΗΤΡΩΟΥ (Α.Φ.Μ.)                         | `employee_tax_indentification_number`           |
| `f_amka`                     | ΑΡΙΘΜΟΣ ΜΗΤΡΩΟΥ ΚΟΙΝΩΝΙΚΗΣ ΑΣΦΑΛΙΣΗΣ (Α.Μ.Κ.Α.)              | `employee_social_security_number`               |
| `f_eponymo`                  | ΕΠΩΝΥΜΟ                                                      | `employee_last_name`                            |
| `f_onoma`                    | ΟΝΟΜΑ                                                        | `employee_first_name`                           |
| `f_date`                     | ΗΜΕΡΟΜΗΝΙΑ ΥΠΕΡΩΡΙΑΣ	                                        | `overtime_date`                                 |
| `f_from`                     | ΩΡΑ ΕΝΑΡΞΗΣ ΥΠΕΡΩΡΙΑΣ (HH24:MM)	                            | `overtime_start_time`                           |
| `f_to`                       | ΩΡΑ ΛΗΞΗΣ ΥΠΕΡΩΡΙΑΣ (HH24:MM)	                              | `overtime_end_time`                             |
| `f_cancellation`             | ΑΚΥΡΩΣΗ ΥΠΕΡΩΡΙΑΣ	                                          | `overtime_cancellation`                         |
| `f_step`                     | ΕΙΔΙΚΟΤΗΤΑ ΚΩΔΙΚΟΣ	                                          | `employee_profession_code`                      |
| `f_reason`                   | ΑΙΤΙΟΛΟΓΙΑ ΚΩΔΙΚΟΣ	                                          | `overtime_justification`                        |
| `f_weekdates`                | ΕΒΔΟΜΑΔΙΑΙΑ ΑΠΑΣΧΟΛΗΣΗ (5) ΠΕΝΘΗΜΕΡΟ (6) ΕΞΑΗΜΕΡΟ            | `weekly_workdays_number`                        |
| `f_asee`                     | ΕΓΚΡΙΣΗ ΑΣΕΕ	                                                | `asee_approval`                                 |

#### Overtime justfications

| **Original API code**   | **Original help text** (in Greek)                                                 | Translation                                 |
|-------------------------|-----------------------------------------------------------------------------------|---------------------------------------------|
| `001`                   | ΠΡΟΛΗΨΗ ΑΤΥΧΗΜΑΤΩΝ Η ΑΠΟΚΑΤΑΣΤΑΣΗ ΖΗΜΙΩΝ                                          | `ACCIDENT_PREVENTION_OR_DAMAGE_RESTORATION` |
| `002`                   | ΕΠΕΙΓΟΥΣΕΣ ΕΡΓΑΣΙΕΣ ΕΠΟΧΙΑΚΟΥ ΧΑΡΑΚΤΗΡΑ                                           | `URGENT_SEASONAL_TASKS`                     |
| `003`                   | ΕΞΑΙΡΕΤΙΚΗ ΣΩΡΕΥΣΗ ΕΡΓΑΣΙΑΣ – ΦΟΡΤΟΣ ΕΡΓΑΣΙΑΣ                                     | `EXCEPTIONAL_WORKLOAD`                      |
| `004`                   | ΠΡΟΕΠΙΣΚΕΥΑΣΤΙΚΕΣ Η ΣΥΜΠΛΗΡΩΜΑΤΙΚΕΣ ΕΡΓΑΣΙΕΣ                                      | `SUPPLEMENTARY_TASKS`                       |
| `005`                   | ΑΝΑΠΛΗΡΩΣΗ ΧΑΜΕΝΩΝ ΩΡΩΝ ΛΟΓΩ ΞΑΦΝΙΚΩΝ ΑΙΤΙΩΝ Η ΑΝΩΤΕΡΑΣ ΒΙΑΣ                      | `LOST_HOURS_SUDDEN_CAUSES`                  |
| `006`                   | ΑΝΑΠΛΗΡΩΣΗ ΧΑΜΕΝΩΝ ΩΡΩΝ ΛΟΓΩ ΕΠΙΣΗΜΩΝ ΑΡΓΙΩΝ                                      | `LOST_HOURS_OFFICIAL_HOLIDAYS`              |
| `007`                   | ΑΝΑΠΛΗΡΩΣΗ ΧΑΜΕΝΩΝ ΩΡΩΝ ΛΟΓΩ ΚΑΙΡΙΚΩΝ ΣΥΝΘΗΚΩΝ                                    | `LOST_HOURS_WEATHER_CONDITIONS`             |
| `008`                   | ΈΚΤΑΚΤΕΣ ΕΡΓΑΣΙΕΣ ΚΛΕΙΣΙΜΑΤΟΣ ΗΜΕΡΑΣ Η ΜΗΝΑ                                       | `EMERGENCY_CLOSURE_DAY`                     |
| `009`                   | ΛΟΙΠΕΣ ΕΡΓΑΣΙΕΣ ΟΙ ΟΠΟΙΕΣ ΔΕΝ ΜΠΟΡΟΥΝ ΝΑ ΠΡΑΓΜΑΤΟΠΟΙΗΘΟΥΝ ΚΑΤΑ ΤΙΣ ΕΡΓΑΣΙΜΕΣ ΩΡΕΣ | `NON_WORKDAY_TASKS`                         |

### Daily schedule

| **Original**           | **Original help text** (in Greek)      | **Translated**                          |
|------------------------|----------------------------------------|-----------------------------------------|
| `f_aa_pararthmatos`    | Α/Α ΠΑΡΑΡΤΗΜΑΤΟΣ                       | `business_branch_number`                |
| `f_rel_protocol`       | ΣΧΕΤΙΚΟ ΕΝΤΥΠΟ ΑΡΙΘ. ΠΡΩΤ.             | `related_protocol_id`                   |
| `f_rel_date`           | ΣΧΕΤΙΚΟ ΕΝΤΥΠΟ ΗΜΕΡΟΜΗΝΙΑ              | `related_protocol_date`                 |
| `f_comments`           | ΠΑΡΑΤΗΡΗΣΕΙΣ                           | `comments`                              |
| `f_from_date`          | ΗΜΕΡΟΜΗΝΙΑ ΑΠΟ                         | `start_date`                            |
| `f_to_date`            | ΗΜΕΡΟΜΗΝΙΑ ΕΩΣ                         | `end_date`                              |
| `f_afm`                | ΑΡΙΘΜΟΣ ΦΟΡΟΛΟΓΙΚΟΥ ΜΗΤΡΩΟΥ (Α.Φ.Μ.)   | `employee_tax_indentification_number`   |
| `f_eponymo`            | ΕΠΩΝΥΜΟ                                | `employee_last_name`                    |
| `f_onoma`              | ΟΝΟΜΑ                                  | `employee_first_name`                   |
| `f_day`                | ΗΜΕΡΑ                                  | `schedule_date`                         |
| `f_type`               | ΤΥΠΟΣ ΑΝΑΛΥΤΙΚΗΣ ΕΓΓΡΑΦΗΣ - ΚΩΔΙΚΟΣ    | `work_type`                             |
| `f_from`               | ΩΡΑ ΑΠΟ (HH24:MM)                      | `start_time`                            |
| `f_to`                 | ΩΡΑ ΕΩΣ (HH24:MM)                      | `end_time`                              |


### Weekly schedule

| **Original**        | **Original help text** (in Greek)                   | **Translated**                        |
|---------------------|-----------------------------------------------------|---------------------------------------|
| `f_aa_pararthmatos` | Α/Α ΠΑΡΑΡΤΗΜΑΤΟΣ                                    | `business_brach_number`               |
| `f_rel_protocol`    | ΣΧΕΤΙΚΟ ΕΝΤΥΠΟ ΑΡΙΘ. ΠΡΩΤ.                          | `related_protocol_id`                 |
| `f_rel_date`        | ΣΧΕΤΙΚΟ ΕΝΤΥΠΟ ΗΜΕΡΟΜΗΝΙΑ                           | `related_protocol_date`               |
| `f_comments`        | ΠΑΡΑΤΗΡΗΣΕΙΣ                                        | `comments`                            |
| `f_from_date`       | ΗΜΕΡΟΜΗΝΙΑ ΑΠΟ                                      | `start_date`                          |
| `f_to_date`         | ΗΜΕΡΟΜΗΝΙΑ ΕΩΣ                                      | `end_date`                            |
| `f_afm`             | ΑΡΙΘΜΟΣ ΦΟΡΟΛΟΓΙΚΟΥ ΜΗΤΡΩΟΥ (Α.Φ.Μ.)                | `employee_tax_indentification_number` |
| `f_eponymo`         | ΕΠΩΝΥΜΟ                                             | `employee_last_name`                  |
| `f_onoma`           | ΟΝΟΜΑ                                               | `employee_first_name`                 |
| `f_date`            | ΗΜΕΡΟΜΗΝΙΑ                                          | `schedule_date`                       |
| `f_type`            | ΤΥΠΟΣ ΑΝΑΛΥΤΙΚΗΣ ΕΓΓΡΑΦΗΣ - ΚΩΔΙΚΟΣ                 | `work_type`                           |
| `f_from`            | ΩΡΑ ΑΠΟ (HH24:MM)                                   | `start_time`                          |
| `f_to`              | ΩΡΑ ΕΩΣ (HH24:MM)                                   | `end_time`                            |

### Schedule work types

| **Original API code**  | **Original help text** (in Greek)   | **Translated**     |
|------------------------|-------------------------------------|--------------------|
| `ΜΕ`                   | ΜΗ ΕΡΓΑΣΙΑ                          | `ABSENT`           |
| `ΑΝ`                   | ΑΝΑΠΑΥΣΗ/ΡΕΠΟ                       | `REST_DAY`         |
| `ΤΗΛ`                  | ΤΗΛΕΡΓΑΣΙΑ                          | `WORK_FROM_HOME`   |
| `ΕΡΓ`                  | ΕΡΓΑΣΙΑ                             | `WORK_FROM_OFFICE` |


## Ports
- [`ergani`](https://github.com/pavlospt/ergani-rust-sdk) Rust SDK by [`@pavlospt`](https://github.com/pavlospt)

## License

This project is licensed under the [`MIT License`](LICENSE)

---

<p align="center">
  <i>🦄 Built with <a href="https://withlogic.co/">LOGIC</a>. 🦄</i>
</p>

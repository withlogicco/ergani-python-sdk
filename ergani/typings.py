from typing import Literal

WorkCardMovementType = Literal["ARRIVAL", "DEPARTURE"]

LateDeclarationJustificationType = Literal[
    "POWER_OUTAGE", "EMPLOYER_SYSTEMS_UNAVAILABLE", "ERGANI_SYSTEMS_UNAVAILABLE"
]

OvertimeJustificationType = Literal[
    "ACCIDENT_PREVENTION_OR_DAMAGE_RESTORATION",
    "URGENT_SEASONAL_TASKS",
    "EXCEPTIONAL_WORKLOAD",
    "SUPPLEMENTARY_TASKS",
    "LOST_HOURS_SUDDEN_CAUSES",
    "LOST_HOURS_OFFICIAL_HOLIDAYS",
    "LOST_HOURS_WEATHER_CONDITIONS",
    "EMERGENCY_CLOSURE_DAY",
    "NON_WORKDAY_TASKS",
]

ScheduleWorkType = Literal[
    "WORK_FROM_OFFICE",  # ΕΡΓΑΣΙΑ (ΕΡΓ)
    "WORK_FROM_HOME",  # ΤΗΛΕΡΓΑΣΙΑ (ΤΗΛ)
    "REST_DAY",  # ΑΝΑΠΑΥΣΗ/ΡΕΠΟ (ΑΝ)
    "NO_WORK",  # ΜΗ ΕΡΓΑΣΙΑ (ΜΕ)
    "REGULAR_LEAVE",  # Κανονική άδεια (ΑΔΚΑΝ)
    "BLOOD_DONATION_LEAVE",  # Αιμοδοτική άδεια (ΑΔΑΙΜ)
    "EXAMINATION_LEAVE",  # Άδεια εξετάσεων (ΑΔΕΞ)
    "UNPAID_LEAVE",  # Άδεια άνευ αποδοχών (ΑΔΑΑ)
    "MATERNITY_LEAVE",  # Άδεια μητρότητας (ΑΔΜΗ)
    "SPECIAL_MATERNITY_PROTECTION",  # Ειδική παροχή προστασίας της μητρότητας (ΑΔΠΠΜ)
    "PATERNITY_LEAVE",  # Άδεια πατρότητας (ΑΔΠΑ)
    "CHILD_CARE_LEAVE",  # Άδεια φροντίδας παιδιού (ΑΔΦΠ)
    "PARENTAL_LEAVE",  # Γονική άδεια (ΑΔΓΟΝ)
    "CAREGIVER_LEAVE",  # Άδεια φροντιστή (ΑΔΦΡΟ)
    "FORCE_MAJEURE_ABSENCE",  # Απουσία από την εργασία για λόγους ανωτέρας βίας (ΑΔΑΠΑΒ)
    "ASSISTED_REPRODUCTION_LEAVE",  # Άδεια για υποβολή σε μεθόδους ιατρικώς υποβοηθούμενης αναπαραγωγής (ΑΔΙΥΑ)
    "PRENATAL_EXAMINATION_LEAVE",  # Άδεια εξετάσεων προγεννητικού ελέγχου (ΑΔΠΕ)
    "MARRIAGE_LEAVE",  # Άδεια γάμου (ΑΔΓΑΜ)
    "SERIOUS_CHILD_ILLNESS_LEAVE",  # Άδεια λόγω σοβαρών νοσημάτων των παιδιών (ΑΔΣΝΠ)
    "CHILD_HOSPITALIZATION_LEAVE",  # Άδεια λόγω νοσηλείας των παιδιών (ΑΔΝΠ)
    "SINGLE_PARENT_FAMILY_LEAVE",  # Άδεια μονογονεϊκών οικογενειών (ΑΔΜΟ)
    "CHILD_SCHOOL_PERFORMANCE_LEAVE",  # Άδεια παρακολούθησης σχολικής επίδοσης τέκνου (ΑΔΠΣΕΤ)
    "DEPENDENT_MEMBER_ILLNESS_LEAVE",  # Άδεια λόγω ασθένειας παιδιού ή άλλου εξαρτώμενου μέλους (ΑΔΑΠΕΜ)
    "VIOLENCE_HARASSMENT_DANGER_ABSENCE",  # Απουσία από την εργασία λόγω επικείμενου σοβαρού κινδύνου βίας ή παρενόχλησης (ΑΔΑΠΣΚ)
    "SICK_LEAVE",  # Άδεια ασθένειας (ανυπαίτιο κώλυμα παροχής εργασίας) (ΑΔΑΣ)
    "DISABILITY_ABSENCE_LEAVE",  # Άδεια απουσίας Α.Μ.Ε.Α. (ΑΔΑΜΕΑ)
    "BEREAVEMENT_LEAVE",  # Άδεια λόγω θανάτου συγγενούς (ΑΔΘΣΥΓ)
    "MINOR_STUDENT_LEAVE",  # Άδεια ανήλικων σπουδαστών (ΑΔΑΝΣΠ)
    "BLOOD_TRANSFUSION_DIALYSIS_LEAVE",  # Άδεια για μεταγγίσεις αίματος και των παραγώγων του ή αιμοκάθαρση (ΑΔΜΑΑ)
    "EDUCATIONAL_LEAVE_VOCATIONAL_TRAINING",  # Εκπαιδευτική άδεια για φοιτητές στο Κ.ΑΝ.Ε.Π. - Γ.Σ.Ε.Ε. (ΑΔΕΚΦ)
    "AIDS_LEAVE",  # Άδεια λόγω AIDS (ΑΔΣΕΑΑ)
    "FLEXIBLE_WORK_ARRANGEMENTS",  # Ευέλικτες ρυθμίσεις εργασίας (ΑΔΕΡΕ)
    "CHILD_CARE_LEAVE_HOURS",  # Άδεια φροντίδας παιδιού (ΩΡΕΣ) (ΩΑΦΠ)
    "PARENTAL_LEAVE_HOURS",  # Γονική άδεια (ΩΡΕΣ) (ΩΑΓΟΝ)
    "FORCE_MAJEURE_ABSENCE_HOURS",  # Απουσία από την εργασία για λόγους ανωτέρας βίας (ΩΡΕΣ) (ΩΑΑΠΑΒ)
    "FLEXIBLE_WORK_ARRANGEMENTS_HOURS",  # Ευέλικτες ρυθμίσεις εργασίας (ΩΡΕΣ) (ΩΑΕΡΕ)
    "PRENATAL_EXAMINATION_LEAVE_HOURS",  # Άδεια εξετάσεων προγεννητικού ελέγχου (ΩΡΕΣ) (ΩΑΠΕ)
    "CHILD_SCHOOL_PERFORMANCE_LEAVE_HOURS",  # Άδεια παρακολούθησης σχολικής επίδοσης τέκνου (ΩΡΕΣ) (ΩΑΠΣΕΤ)
    "OTHER_LEAVE",  # Άδεια Άλλη (ΑΔΑΛ)
    "OTHER_LEAVE_HOURS",  # Άδεια Άλλη (ΩΡΕΣ) (ΩΑΑΛ)
]

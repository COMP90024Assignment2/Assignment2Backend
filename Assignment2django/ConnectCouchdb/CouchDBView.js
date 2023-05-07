// median_mortgage_repay_monthly,  median_rent_weekly, median_tot_fam_inc_weekly, gccsa_code_2021
const sudo_city = function (doc) {
    emit(doc.gccsa_code_2021, {
        median_mortgage_repay_monthly: doc.median_mortgage_repay_monthly,
        median_rent_weekly: doc.median_rent_weekly,
        median_tot_fam_inc_weekly: doc.median_tot_fam_inc_weekly
    });
}


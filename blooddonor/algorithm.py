from .models import Donor

# Blood group compatibility chart
COMPATIBILITY = {
    'A+':  ['A+', 'A-', 'O+', 'O-'],
    'A-':  ['A-', 'O-'],
    'B+':  ['B+', 'B-', 'O+', 'O-'],
    'B-':  ['B-', 'O-'],
    'O+':  ['O+', 'O-'],
    'O-':  ['O-'],
    'AB+': ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-'],
    'AB-': ['A-', 'B-', 'O-', 'AB-'],
}

def calculate_score(donor, requested_blood, requested_district):
    score = 0

    # Step 1 - Blood compatibility (50 points)
    compatible = COMPATIBILITY.get(requested_blood, [])
    if donor.blood_group in compatible:
        score += 50

    # Step 2 - Same district (30 points)
    if donor.district.lower() == requested_district.lower():
        score += 30

    # Step 3 - Donor is available (20 points)
    if donor.is_available:
        score += 20

    return score  # max = 100

def find_donors(requested_blood, requested_district):
    donors = Donor.objects.filter(is_available=True)

    # calculate score for each donor
    scored = []
    for donor in donors:
        score = calculate_score(donor, requested_blood, requested_district)
        if score > 0:  # only include compatible donors
            scored.append({
                'donor': donor,
                'score': score,
                'name': donor.user.get_full_name(),
                'blood_group': donor.blood_group,
                'district': donor.district,
                'phone': donor.phone,
            })

    # sort by score - best match first
    scored.sort(key=lambda x: x['score'], reverse=True)

    return scored
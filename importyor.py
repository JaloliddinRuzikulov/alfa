for index, row in df.iterrows():
    user = User.objects.filter(student_id=row["ID"]).first()
    if user is not None:
        payment = row["To'langan summa"]
        direction_contract_a = DirectionContract.objects.filter(direction_id=user.specialty.id, study_type=user.study_type, academic_year_id=4).first()
        direction_contract_b = DirectionContract.objects.filter(direction_id=user.specialty.id, study_type=user.study_type, academic_year_id=1).first()
        student_contract_sum_a = StudentContractSum.objects.filter(student=user, academic_year_id=4).first()
        student_contract_sum_b = StudentContractSum.objects.filter(student=user, academic_year_id=1).first()
        difference_sum = int(direction_contract_a.contract_sum) - int(payment)
        if difference_sum >= 0:
            student_contract_sum_a.summ=int(payment)
            student_contract_sum_a.save()
        else:
            student_contract_sum_a.summ = direction_contract_a.contract_sum
            student_contract_sum_a.save()
            student_contract_sum_b.summ=(difference_sum * (-1))
            student_contract_sum_b.save()
    else:
        print(f"No user found with ID {row['ID']}")

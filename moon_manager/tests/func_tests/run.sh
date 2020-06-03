#!/usr/bin/env bash
# pip install behave astropy

mkdir -p logs

echo -e "\033[31massignments.feature\033[m"
behave --junit features/assignments.feature  | grep -vE "^    "
echo -e "\033[31mdata.feature\033[m"
behave --junit features/data.feature  | grep -vE "^    "
echo -e "\033[31mmeta_data.feature\033[m"
behave --junit features/meta_data.feature  | grep -vE "^    "
echo -e "\033[31mmeta_rules.feature\033[m"
behave --junit features/meta_rules.feature  | grep -vE "^    "
echo -e "\033[31mmodel.feature\033[m"
behave --junit features/model.feature  | grep -vE "^    "
echo -e "\033[31mpartner.feature\033[m"
behave --junit features/partner.feature  | grep -vE "^    "
echo -e "\033[31mpdp.feature\033[m"
behave --junit features/pdp.feature  | grep -vE "^    "
echo -e "\033[31mperimeter.feature\033[m"
behave --junit features/perimeter.feature | grep -vE "^    "
echo -e "\033[31mpolicy.feature\033[m"
behave --junit features/policy.feature  | grep -vE "^    "
echo -e "\033[31mrules.feature\033[m"
behave --junit features/rules.feature  | grep -vE "^    "

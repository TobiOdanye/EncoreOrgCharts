import pandas as pd
import requests
import re
import io
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe

# Set options to display all rows and columns
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Optional: widen the display if needed
pd.set_option('display.width', None)

def fetch_api_tokens():
    api_tokens = [
        "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzIiwianRpIjoiOTNkOWE1NTRiNTBkMDJkZDlkYTQzMDIzYWU5OTM2ZGRkZ"
        "GEyNmU1YjRkMDYxMzFhNGFiYzc2NDNkMjY4YTYxN2ZlZjY4NjJlZWVmZjVjMTgiLCJpYXQiOjE3MzY0MzA4NjYuODkzNjM0LCJuYmYiOjE"
        "3MzY0MzA4NjYuODkzNjM5LCJleHAiOjQ4OTIxMDQ0NjYuODg4ODAzLCJzdWIiOiIxOTc0ODU3Iiwic2NvcGVzIjpbXX0.DtP-949ngXZ4N"
        "PEW9aAaPxK9pcb7WOuru35ZzDCFWv-i2OwefloSIPIn6Q75Gd7EM5-1PNp55kpl5IENS_CXI3Xo0x4P_a9YHwXerWhbylEcVauB_oE5JIV"
        "laA5d9yQhbrv7Xf2wzBMP7By0ANcpqobAl7ld_DgVF-YA5zzhvhh2itAbtnXOv8jG_K56BhfECwC9HK2J2vihVJmgxWp_n9jjZShOMnlTz"
        "Rf4OIf0bUPLtZV3tI1VlyTLoR0kBH4Osu6uYHw5QkMqAil23uuDqopHaAI-6w1U9tWuZV7PkS_tdkbjpGYgeKLdm6gpenFyVLcUzyAySoE"
        "Z2NH5eKCLg_TPOw7BxJGjY_K15UpBl0EIe59zZjtwZA_CW1QfhRAS27MwA-7TDkPNeQWNKFn8TdlsySidHI7J7lfmG0KB4793pUMjljvA3"
        "_wvh1ZKnplFQ10y_fXcmCyuQrKM44Vl6ZaLD78wQ-q_fN88tSaV4Avq1Z80XzsTfJEkfoG2Lnpa61760CyXG0v3l6R0i_U4SQk1FdwhuPp"
        "_cP3hLyu9BrFLRt4u53lMmTa_5J72rRzbGBVeZjjJBOXFy3Y9J-OM7H4u4Kz0QIZhyN3XB2lXgHy7VZcsRuQhb6X39W3Ukk0ZyuCZeEWK4"
        "mn_Uf7i9d4uiDuLalRhu-vHXpOHsyAvQl0",
        "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzIiwianRpIjoiMjM5Y2Q1N2I0MGI1MjBhN2Y5NGRhMzE0ZjdlMDIwMm"
        "JkMmViNDFjNjU5YTkxNjRhOTRjYWEwZjRkOTYzOTFiMjkxNzY5NzNiNzAwYTJlODIiLCJpYXQiOjE3MzM4NDczNDguOTkyNzQyLCJuY"
        "mYiOjE3MzM4NDczNDguOTkyNzQ1LCJleHAiOjE3NjUzODMzNDguOTc1NTAyLCJzdWIiOiIxOTczNjY2Iiwic2NvcGVzIjpbXX0.jgIg"
        "ZkAsB-Ncivv5lyJCQx3XvABRbIpUThmLtb7AENe0S8e3lwKSBkyE_QbrFqIYa-z4p0J42OkQz0uv-h_aepG_7OhdlKzpe3eSECZY1LE"
        "RRtqdTIsO9gBx0Wqxul7ixOaAJHdjpHCHS_eXaZKLu3_OhTEkyAD8EHILlbv6Uc3R2cOtpY5s3rJEFffcPIN7tmuZ7Mmeo9SJXpnSdb"
        "4qg6REJsO5YLFPUpvZyZn1G9SwVfpZAP0nfbrTuXKIwo6gbX22R_UZGL_n2rHnObUqKyRUdS8XCEuZfQNge6_VwT2vsb72rNMK4Dw5S"
        "m4jeQEcdbRMaB-rr0YpkFXyMAhHsV8cimfmDPro_NxUV2dXONtlfZhGFySPbAckncCZq7geMLXhP-MYOm3FxPsiI7FFw3_LsQyNICs4"
        "Hndy8ccKe_sPldWWV6eq7E2OYQcpOfrcRjk4YrnVl1fJL_krxVYvf_JwYqRb9GCpjpdBScWlKWc549HnqKtx-jD8S_QOjgDCuVgXwbg"
        "wggmcKLCb9AEAL3zcKwOSoxQ4Bqg8XMqHLiSoUs-KwHxj6bpi1xXzeaCTN84sV1jK4TO99v_bjHGkBSP9H6sbwEViPdaD9MmjMOv0C5"
        "z-PdGTf7cRQm6kee0F7Q6gk7J-nRBGV5unL0il7S9gd2UXZc7xsJV3hkm8Qws",
        "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzIiwianRpIjoiNWY1NGY5NzBmMWJlNDEyNDUwZGI2ZjczMWRjNzA2NTI"
        "4NmVkMzRhMGQxMGVkODZmYzY0OWI1NWFlN2E1MWE1M2Q4M2Q2N2FhMjAwNTk2ZGIiLCJpYXQiOjE3MzY3OTAzMzQuOTYzNjE3LCJuYmYi"
        "OjE3MzY3OTAzMzQuOTYzNjIsImV4cCI6NDg5MjQ2MzkzNC45NTc0NTMsInN1YiI6IjE5NzUwNzUiLCJzY29wZXMiOltdfQ.f-nZneDlXj"
        "G8cAk8VJuvJYBw9jBToBx3cL-I2uFqTjvhoX4oqoYsAQPvTIMhOJLXwL8yYxl1bPWro7ynjx-HiZu0w5PylnZzDPWxZQlBCYluLIOIoel"
        "4_mdpZvF0Jb-755dWLkWsT9Yxn86PjwtDqDizZzXGML8r3TIwlFwD03wSMvOKdZK7Uc7x8u2NZBq4jIS7eZM0sQtM5dciyPEk8S03Z5TG"
        "MUxye2zWAp9iAXXRStdPGs1pwe3UTWIjbyMBTLMmUDuKYzixXOVmzkkyL5IiqGfrbm4fHfk4s-C4B8jnFnUpkaGtGGAaT8mdKJmjNeFla"
        "1xg3XG306TSJ7dfYDV9NyGav0okQbERSPL5wRG9m9CrgMdzad7U08MuV8glST3koHY0TZguNtL-G4m7luPfQIK26EXmrCJI2jL7keBgcU"
        "N9Pck0hmUQiCbyn01L-rC8pU6i-R4a9mqKYVtlOfDHTcSuUyPtoa1EE-WA-rSY4cLtTtRqwJUCv3_1rQ2lhMfe0TfL-DRDvwfhyxF8xy0"
        "kygYPfs83wL4UkxTZxZnsAUjv51G-302ZLqrBVLkODOSLmAWJgLBu1BsvW7bKXUwQCLcut2RfPn9OhnS75Tu3qUvAq7uXNwNPH6zw0j53"
        "9rOlHt3A4TgkFiOZzjKvBhr1WT7ZuzHWUYPvLjdv1fw",
        "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzIiwianRpIjoiNTAwZmIyNDU4OWVmYmI4MWRiNmVmMmJhZmI3ODA1ZjEy"
        "ZTIyN2RjM2NhMjYzNmYzYzI1NGY3ODI5ZDlmMmFiYzEwMjllN2EwMTUyNjBiNGYiLCJpYXQiOjE3MzY4NTEzODUuNDg0MDU3LCJuYmYiO"
        "jE3MzY4NTEzODUuNDg0MDYsImV4cCI6NDg5MjUyNDk4NS40Nzk5NDUsInN1YiI6IjE5NzUxMTAiLCJzY29wZXMiOltdfQ.iXjyYV6C7zj"
        "Z6-f6KZ3EFrdS_R1ntjv4X-LgV4wZqz5wHRVM1AbotaDJi2dtuFVludJWBhXlLEu32FpsB1Ogrk0pBe2ELB3HcN6Rc80uUBHUDo8Xbtux"
        "e_dhtOcP9ZsDEltDsvSBznzGWUSqaxHu3BxpBfhlmLwzjhbA2SLkKbMo_LnlnuenpKSAxnpwExuuvY4znPLZhSBHdfdPABdkchPfCX7Js"
        "Lp58ZvMqyZ8zjJ1fRcjfpBz6VybxIW9oErtGRsXfdU5eUX6hW2MWgtNkW6iU09k_Ge4C7ag4QaQTWkLkM2DjLOoLByXm3b1URv04suYDK"
        "FGAUmO9zapAqjYJ2ljp8yrqpRnLnmr7ltQHQ-nZezUQZJDdvIM5kWANLMQEax9xPAB6EbTouXFf8X8NjiCtbAAJcPPLAHsxPX5CW9DVMW"
        "-tw1zsHC06Jg_ou3LMd-XUPilF86iXC_1pP_0dbgCDa7GZEaV_ptiQ24LqD1QSkKt7qXVvxmoO2Ktu4mJez1tzs6prThke9YiijG9FJND"
        "a4Tnj6K_DCsx_IJwaoCBFQjM7l_EaIAYTgh49nPojPGfXop-_oIxcEhJN1ZH26syhC2rARV84vQ30h1VerRWWddWP8mxjx0lIv3oRiG6v"
        "gvyR-iD9nyVW41NOykKGDv9GaAexB4PkgRJ7pjUkFw",
        "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzIiwianRpIjoiYjFjZGU4ZmNiOGM2MjQxZWVkN2E3ZDk3NDhmMWJlMzgyY"
        "Tc2MmY2ZjBkZjI0NmY4MGFmZjJkMjA0NmJmYjZiZTAwM2ExNzY5YTVlYzYzMDciLCJpYXQiOjE3MzY5NTQzMDUuNjA3NzIyLCJuYmYiOjE3"
        "MzY5NTQzMDUuNjA3NzI1LCJleHAiOjQ4OTI2Mjc5MDUuNjA0MDEyLCJzdWIiOiIxOTc1MjI1Iiwic2NvcGVzIjpbXX0.oFYuSb5P0ESf7cH"
        "tHVGqR-2FMwUKycawpb_gUKAqzOzPf_-y5yri8AyK8-ssKZ7-hZn4utzMTxHmeJ8rFWCpW1rrJhI1EfrcjqDS_z4P_smbDEeIwABVLBvm4t"
        "fZCQAGwHSvt7SEIfjP_YNU5R2sF_natkqqAvqCdzmcmJoLJP6-kCO5vlOwsTKtYQhus7IKeyHbyXBqdAm5MXi85uLeeZvYlu-BIcwiN6xwe"
        "aLSyBlR44gqiliDsAbb0GmQ9IFQq2Mjmt7m3ajsVdF_HeQJVZyvSKTn_QEZ9rp40x7CwaYxsECcmBfUTWbTs5fdj3ZUznvnn6yFOFzTt0IY"
        "yvRo-v0ZDiIOMqNVJ5jzQXlBUb39YHljKVLZBQguC4UijWIOTkpGpbhLNaueO3FjwBPji0jqCIblxmyRC3QhzTEJOJcduAV8HSh7sILkWoA"
        "x05j2ShRPhu9ri2uIGZzEL2_H27CKqWIap66MCWz0npfPgH1L1LHiOKxIK9oV1X7fUJM9ol1KAHmacrT88y-JotHgKqcd1GseVWLQzlm3-o"
        "Q0-LIiwbSZOfIHSF3a8u5MGhtGrtVTEQnxubQ-rfo6IKTCWHAj_zc3DdySdsmakejZ7_JkLDP414JkGgFEiMhB9tz3weOsCavHPm80cjr2P"
        "bAb6NTWFlMTy-AyMSsq60b85jA",
        "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzIiwianRpIjoiNjQ4MjQzMWI3ZWMwZGMwYTVmMWYxY2Q2ZDdjMThiZjkyOW"
        "FmYjljNDhjNmY2MDI2YTdkMWVjZjMyNWJiY2Q0MjY3MGU2ZjFmNjdkNjIxMTAiLCJpYXQiOjE3MzY5NTQzNzMuMjI1MDAzLCJuYmYiOjE3M"
        "zY5NTQzNzMuMjI1MDA3LCJleHAiOjQ4OTI2Mjc5NzMuMjIwNDM0LCJzdWIiOiIxOTc1MjI2Iiwic2NvcGVzIjpbXX0.EEs7cwr17uZ7E-Mj"
        "jYNehnhkcuWEhVF-HIQEU78pLpv0_8MxgIF0KufjHwb60hhdlh2kuNh2DKssq8F7E3aHvPXYOtrnYQvq4GBLM0Q2LeRG3dKduCdC6iBC0h4"
        "EJX3DlJ-yWfRbjmcURjAC0wPCU0_5rv89eLLZJRWAYTJIS1X1MXhvkt1fu0DsQl3PdbZ-EaWRdp88CgK9RTDtwx4V-mNLp_WrhZ541D_fbw8"
        "ZVcISMPMRRhhetDxB3mBrLkWt23A44uPS4Kq4vHPNwBxzLhIgBtdcm-PAqitFnfC4p5b9V_ntWXLTkcEY2X7LoI1xwYh8OIZaXjiLdBqJOP"
        "tifdLXaeW_diGgr6SoUngNN2WE-tY0U9PKx_Xua8-kSitMZFnwKPOmKA2CqOgLy97sG_eA1LF8bY3krYqVS8B9vnfT1_KEotcQO5LYiTM6fR"
        "vWK9Ki9CLBVmot6Bv7XYOWoF7DQgFx7jEGmWGV3HR1P1SOgDZ9ZZaOxPm8RIDUPmVrc2CocWkWTbYa0wE5KwrnzZT5GDBxJp5QCQyjQ_7rhv"
        "jMeO8FQxOqJTvIE5iKmoBDUqUr4G58XNYVdBxi9xcnsQSCHU8VRUlGdFYP0r71sFMmzQCqOY7hu84odb1aS3_vko7yynm54wfGO8auG7pgqS"
        "fRM5_84z9y4BaLzbRDyFQ"]
    return api_tokens

def fetch_hotlist_candidates(api_id, api_tokens):
    candidate_list = []

    # Ezekia URL
    base_url_agg = f"https://ezekia.com/api/projects/{api_id}/candidates?filterOn%5B%5D=fullName&sortOrder=desc&sortBy=createdAt"

    # Headers to authenticate API request for total counts
    headers = {
        "Authorization": f"Bearer {api_tokens[0]}",
        "Content-Type": "application/json"  # Adjust content type if necessary
    }

    # API request (GET request) for total counts
    page_response = requests.get(base_url_agg, headers=headers)

    # Extract "last_page" value
    last_page_candidates = page_response.json()['meta']['lastPage']

    # Loop through candidates in hotlist
    for page in range(1, last_page_candidates + 1):

        api_token = api_tokens[(page - 1) // 3 % len(api_tokens)]

        # Headers to authenticate API request for total counts
        headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"  # Adjust content type if necessary
        }

        page_url = f"https://ezekia.com/api/projects/{api_id}/candidates?filterOn%5B%5D=fullName&page={page}&sortOrder=desc&sortBy=createdAt"
        page_response = requests.get(page_url, headers=headers)

        for candidate_index in range(0, len(page_response.json()["data"])):

            if page_response.status_code == 200:
                # Process the data for this page (you can print or store it)
                print(f"Ezekia API ID {api_id}")
                print(f"Fetched candidate page {page} from Ezekia API")
            else:
                print(f"Failed to fetch data for page {page}. Status Code: {page_response.status_code}")

            # Candidate details
            candidate_id = page_response.json()["data"][candidate_index]["id"]
            candidate_name = page_response.json()["data"][candidate_index]["name"]
            candidate_updated = page_response.json()["data"][candidate_index]["updatedAt"]

            if len(page_response.json()["data"][candidate_index]["addresses"]) > 0:
                if page_response.json()["data"][candidate_index]["addresses"][0]["city"]:
                    candidate_city = page_response.json()["data"][candidate_index]["addresses"][0]["city"]
                else:
                    candidate_city = ''

                if page_response.json()["data"][candidate_index]["addresses"][0]["country"]:
                    candidate_country = page_response.json()["data"][candidate_index]["addresses"][0]["country"]
                else:
                    candidate_country = ''

            else:
                candidate_city = ''
                candidate_country = ''

            #candidate_address = candidate_city + ', ' + candidate_country

            # Candidate position details
            candidate_position_data = page_response.json()["data"][candidate_index]["profile"]

            # Iterate through each position and dynamically name the fields
            for index, position in enumerate(candidate_position_data['positions'], start=1):

                candidate_role_number = index

                if 'title' in position and position['title'] is not None:
                    title = position['title']
                else:
                    title = None

                if 'company' in position and position['company'] is not None and 'name' in position['company']:
                    company = position['company']['name']
                else:
                    company = None

                if 'location' in position and position['location'] is not None and 'name' in position['location']:
                    location = position['location']['name']
                else:
                    location = None
                    #location = candidate_address

                if 'industry' in position and position['industry'] is not None and 'name' in position['industry']:
                    industry = position['industry']['name']
                else:
                    industry = None

                if 'startDate' in position and position['startDate'] is not None:
                    startdate = position['startDate']
                else:
                    startdate = None

                if 'endDate' in position and position['endDate'] is not None:
                    enddate = position['endDate']
                else:
                    enddate = None

                if 'summary' in position and position['summary'] is not None:
                    summary = position['summary']
                else:
                    summary = None

                # Dynamically creating field names
                candidate_role_number = index

                # Create a dictionary with dynamically named fields and print it
                position_info = {
                    "Candidate Experience": candidate_role_number,
                    "Candidate Title": title,
                    "Candidate Company": company,
                    "Candidate Location": location
                }

                # New key-value pair to add at the start
                candidate_dict = {'Candidate ID': candidate_id,
                                  'Candidate Name': candidate_name,
                                  'Candidate Updated At': candidate_updated}

                candidate_info = {**candidate_dict, **position_info}

                # Append extracted values to the list
                candidate_list.append(candidate_info)

    # Create a DataFrame from the list of candidate data points
    candidate_df = pd.DataFrame(candidate_list).reset_index(drop=True)
    print(candidate_df.info())

    #candidate_df['candidate_start_date'] =
    candidate_df['Candidate Location'] = candidate_df['Candidate Location'].replace('United Kingdom', 'London, UK')

    return candidate_df

# Normalize and map fallback + bracket values to final form
fallback_map = {
    'executive director': 'ED',
    'managing director': 'MD',
    'vice president': 'VP',
    'vice-president': 'VP',
    'vp': 'VP',
    'md': 'MD',
    'ed': 'ED',
    'assoc': 'As',
    'assoc.': 'As',
    'as': 'As',
    'an': 'An',
    'analyst': 'An',
    'director': 'D',
    'd': 'D'
}

# Normalize and map fallback + bracket values to final form
ordered_fallback_map = {
    'managing director': 'MD',
    'executive director': 'ED',
    'director': 'D',
    'vice president': 'VP',
    'vice-president': 'VP',
    'vp': 'VP',
    'md': 'MD',
    'assoc': 'As',
    'assoc.': 'As',
    'analyst': 'An'}

# Ordered list for substring matching
ordered_fallbacks = list(ordered_fallback_map.keys())

# Approved values for brackets (case-insensitive)
allowed_bracket_values = set(fallback_map.keys())


def extract_seniority(text):
    text_lower = text.lower()

    # 1. Try to extract and validate bracketed content
    bracket_match = re.search(r'\(([^)]+)\)', text)
    if bracket_match:
        bracket_value = bracket_match.group(1).strip().lower()
        if bracket_value in allowed_bracket_values:
            return fallback_map[bracket_value]

    # 2. Fallback to substring search
    for keyword in ordered_fallbacks:
        if keyword in text_lower:
            return fallback_map[keyword]

    return None  # or 'Unknown'


def fetch_candidates_additional_labels(hotlist_df_trans, api_tokens):
    candidate_id_list = list(hotlist_df_trans['Candidate ID'].unique())
    print(f"Total candidates: {len(candidate_id_list)}")

    candidates_additional_list = []
    index_counter = 0
    for index, id in enumerate(candidate_id_list):

        print(f"Project: {index} / {len(candidate_id_list)}")

        candidate_url = f"https://ezekia.com/#/people/{id}"

        # Ezekia URL for total meeting and page (api) count
        base_url_agg = f"https://ezekia.com/api/relationships?id={id}&type=person&relatedType=person"

        index_counter += 1
        api_token = api_tokens[(index_counter - 1) // 3 % len(api_tokens)]

        # Headers to authenticate API request for total counts
        headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"  # Adjust content type if necessary
        }

        # API request (GET request) for total counts
        response = requests.get(base_url_agg, headers=headers)

        # Initialize project_rec_label before the loop
        candidate_reports_into = None

        # Iterate through the response data
        response_data = response.json()
        if "data" in response_data and "people" in response_data["data"]:
            for person in response_data["data"]["people"]:
                if person["relationship"] == 27571:
                    candidate_reports_into = person["id"]

        # Append extracted values to the list
        candidates_additional_list.append({"Candidate ID": id, "Candidate URL": candidate_url, "Candidate Reports Into": candidate_reports_into})

    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(candidates_additional_list).reset_index(drop=True)

    return df

def get_candidate_companies(group):
    # Sort by experience
    group = group.sort_values(by='Candidate Experience')
    
    # Get company for experience 1
    company1 = group.loc[group['Candidate Experience'] == 1, 'Candidate Company'].values[0]

    # Find the first different company
    different_company_row = group[group['Candidate Company'] != company1]
    if not different_company_row.empty:
        company2 = different_company_row.iloc[0]['Candidate Company']
    else:
        company2 = None  # or np.nan or ''

    return pd.Series({
        'Candidate ID': group['Candidate ID'].iloc[0],
        'Candidate Company Previous': company2
    })
    
# Streamlit UI
st.title("Ezekia Org Chart Inputs")

# Input
api_id = st.text_input("Enter Ezekia Project API ID")

if st.button("Fetch Candidates") and api_id:
    try:
        api_tokens = fetch_api_tokens()  # Get tokens here
        candidates = fetch_hotlist_candidates(api_id, api_tokens)
        st.success("Fetch hotlist candidates function 1!")
        candidates_previous = candidates.groupby('Candidate ID').apply(get_candidate_companies).reset_index(drop=True)

        candidates = candidates.merge(candidates_previous, on='Candidate ID', how='left')
        candidates = candidates[candidates['Candidate Experience'] == 1]
        
        candidates['Candidate Seniority'] = candidates['Candidate Title'].apply(extract_seniority)
        candidates = candidates[[ 
            "Candidate ID", "Candidate Name", "Candidate Title",
            "Candidate Company", "Candidate Location", "Candidate Seniority", "Candidate Company Previous"
        ]]
        
        candidates["Lucid Space"] = ""

        candidates.loc[candidates['Candidate Location'].str.contains('Paris', case=False, na=False), 'Candidate Location'] = 'Paris'
        candidates.loc[candidates['Candidate Location'].str.contains('London', case=False, na=False), 'Candidate Location'] = 'London'
        candidates.loc[candidates['Candidate Location'].str.contains('New York', case=False, na=False), 'Candidate Location'] = 'New York'
        candidates.loc[candidates['Candidate Location'].str.contains('Singapore', case=False, na=False), 'Candidate Location'] = 'Singapore'
        
        candidate_reports_into = fetch_candidates_additional_labels(candidates, api_tokens)
        candidates_output = pd.merge(candidates, candidate_reports_into, on='Candidate ID', how='inner')
        
        st.success("Data fetched successfully!")
        st.dataframe(candidates_output)

        service_account_info = {
            "type": "service_account",
            "project_id": "ezekiastreamlitlucid",
            "private_key_id": "0037661e3160a0b0c74eedfdb8de8e09d02c9f90",
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDOdFqt02WP9U++\nj/UTEWV/SprBLAAYlcqERy4WqKUD/oiKj+z5dzWCfel9JGLWka4RHsK8Gr6qOffh\ngfQd3ae+2g+GroSqtLD1yZtrSFsZTGFpObjTqqJ/9v3fYnuv8E2k9XbJCSAFzxMJ\nzAZ7oaEK26zXsOQnPiTvErcE6zy3G4BbB4EB82gj14Psl5KgTDIHDHUt7uy2qp4D\nH8dJoAl1Vp8Okn6KNGKrpRamxLZudFOjfFt20KDjycbT78ueSoG9F+hOZ/Nl5/0s\nmrgzHih/t2194SG08Ax/vqv0m79X+WEH4e8ONMRqkL9JmYBsq5D7xLhT5Q1fczfV\nP0NKCVjBAgMBAAECggEANGAMSSDiGR1Qt7VppQa6ywowLGVvOM13bQtpw9HQ2yyN\nkylkIv19E7fBrj+221xl3m4BVRsr15+RJSKEvbbnwWEsoyxO98eTRSd6SEM46TgZ\nVkqQexJE21XbnfosCrxZ1kl3cxTfjNm1qLybwG2Gn2yPcsCrgNEhKY2D5LmQ05qv\n1Y9v2TsoSWIv7stOpe/mtw/RE3TeEvFM1MvABPAxb0guIz5AP0+jYLulK/T0geeT\n0IhPTeThxa4PdC2jIirG3/2hXtbxNA63D65euBMF1hMwcKy/fZr9H/l8y3CYkJRV\ntBR1Wul2YDz67JUj0VRAJKosS7BAcAdT4hoW+PCOyQKBgQDnLNXFNLO9oAcMNq8h\nlGNKuiAcS33NTj1YuHeERXzlzyKMOcv5USQzkRC7R8ztXRPckAglcspaHVhS2buc\n+21yT7LSqOF/tn59US5HL8q4Vc/JFkFjtfQ6TZNxTqbQDZOgWAumxogAPspFoji+\niO+/wESc4yJXO++7hEHHcbkZfwKBgQDkn+6UGLZL34PUPB/5S71ZYbOmtw1qTfvD\nZXCp/AjtRem2VNiyh4ANWL05OaxMpGwcKsOSlTCf+uPPCPAazp/yWErbX/wmd2Wi\nALmrZMvo/KaoEk2b5n6BINpBv2cnYZpoc9CYDJEAArRZio1/HlX0gnKSxhXjIEij\nMElBCowtvwKBgQCLbXA1M9cgjG8Tv7ua7iuAu4d4aVOjyweXBhMXlO2CkY6NsqJC\nad0CuQC1Y9XGZ7f99GTlaTmAZmiJ98Z/JOna4xTAl5kB9SiPHrJhvwJucVsUNjcU\nE38M1xMRaNWVcErUj6XfXahTNYu7ud6tlFu9dBIt6ZQhtwWdPGSMDRwNswKBgCk+\njPzcpG51qUOtgRspRcSNMqq91Ua7QNMURsnztOyRM0N4dQtoFHrT6ncbZ3EALJy8\nPkIAdiA2U8iy1RYQ9pvyv7Zpz4Rk/8nFFbnM2lhy0+H4Q1X/tAy5j4ZS8FoTapaz\nZgs4ISR+WGja7QHkyB7vNZoy8BnkZhZCjMSWEYnjAoGBALXU0C7Bl9xG/X00WTN+\nz0hkqN739oRal+E34k6RP5QrUzNtG1v3jdfvX1hDBfKvUR+ybhf/f3+ggrMpHCUo\nGQ3G3XBxWbVgmuEkjtYAGUQ+XREru3U55UYG1pBNspwU96ZHtzsAwqTvumtmgPK6\nY9/hHjMb6ORsGFCk78MfuDtA\n-----END PRIVATE KEY-----\n",
            "client_email": "ezekiastreamlitlucid@ezekiastreamlitlucid.iam.gserviceaccount.com",
            "client_id": "102616053130023320317",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/ezekiastreamlitlucid%40ezekiastreamlitlucid.iam.gserviceaccount.com",
            "universe_domain": "googleapis.com"}

        # Define scope and authenticate
        scope = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("serviceaccountkeys.json", scope)
        client = gspread.authorize(creds)

        # Open Google Sheet and worksheet
        sheet = client.open_by_key("1kDZIOe5orm-OCaeCRxtSEmVU8kkoNdF_23zNj_0GHW0")
        worksheet = sheet.worksheet("LucidData")

        # Clear the worksheet and write new data
        worksheet.clear()
        set_with_dataframe(worksheet, candidates_output)

        # Excel export
        # excel_buffer = io.BytesIO()
        # with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
        #    candidates_output.to_excel(writer, index=False, sheet_name='Candidates')

        # st.download_button(
        #   label="Download Excel",
        #   data=excel_buffer.getvalue(),
        #   file_name="ezekia_candidates.xlsx",
        #   mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        #)

    except Exception as e:
        st.error(f"Error occurred: {e}")


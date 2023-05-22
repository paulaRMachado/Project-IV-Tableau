import pandas as pd



def kaggle_basic_clean(df):
    """
    This function removes from the dataframe some unnecessary columns, drops rows with missing values
    arg:
    :df: dataframe to be cleaned.
    
    returns:
    :clean_df: returs the dataframe without unnecessary data
    """
    df.drop(columns=["participant_relationship","address","location_description","participant_age","incident_id","participant_status","source_url","incident_url","incident_url_fields_missing","congressional_district","sources","participant_name"], inplace=True)
    df.dropna(subset=["latitude","participant_type"], inplace=True)
    return df

def wiki_basic_clean(df):
    """
    This function removes from the wiki table some unnecessary columns and corrects datatypes
    arg:
    :df: dataframe to be cleaned.
    
    returns:
    :clean_df: returs the dataframe without unnecessary data
    """
    df.drop(columns=["State Rank","2019","2012","2011","2010"], inplace=True)
    
    columns_dollar = ["2018", "2017", "2016", "2015", "2014", "2013"]

    for column in columns_dollar:
        df[column] = df[column].str.replace("$", "")
    
    return df

def mode_list(value):
    """
    """
    # Check if the value is a Nan
    if pd.isnull(value):
        return None

    split_values = value.split("||")

    split_values = [v.split("::")[1] if (len(v.split("::")) > 1) else None for v in split_values]
    
    non_null_values = [v for v in split_values if v is not None]
    if len(non_null_values) == 0:
        return None
    
    mode_value = pd.Series(non_null_values).mode().values[0]
    
    return mode_value

def basic_transf(df):
    """
    This function transforms
    """
    df["gun_stolen"] = ["Stolen" if "Stolen" in i else "Not-stolen" if "Not-stolen" in i else "Unknown" for i in df["gun_stolen"].fillna("Unknown")]
    df["n_victims"] = [i.count("Victim") for i in df["participant_type"].fillna("0")]
    df["n_suspects"] = [i.count("Subject-Suspect") for i in df["participant_type"].fillna("0")]
    df["n_women_involved"] = [i.count("Female") for i in df["participant_gender"].fillna("Unknown")]
    df["n_men_involved"] = [i.count("Male") for i in df["participant_gender"].fillna("Unknown")]
    
    # Standardize weapon type
    weapon_types = {"AK-47":"Machine Gun","Auto": "Automatic","gauge":"Shotgun","Shotgun": "Shotgun","Win":"Rifle","22 LR":"Rifle",
                "Rifle":"Rifle", "AR-15": "Rifle","Spr":"Rifle","9mm":"Handgun","Handgun":"Handgun","SW":"Handgun","Mag":"Handgun",
                "10mm":"Handgun","38 Spl":"Handgun", "Unknown": "Unknown", "Other": "Unknown", "":"Unknown"}

    search_dict = {k.lower(): v for k, v in weapon_types.items()}

    df["gun_type"] = df["gun_type"].map(lambda x: search_dict.get(next((i for i in search_dict if i in str(x).lower()), x), x))
    
    condition1 = df['gun_type'] == "Unknown"
    condition2 = df.incident_characteristics.str.contains("BB/Pellet")
    df.loc[condition1 & condition2, 'gun_type'] = "BB/Pellet"


    # Standardize incident type
    incident = {"mass":"Mass shooting","Non-Shooting":"Non-Shooting Incident","invasion":"Home Invasion","robbery":"Armed robbery","Defensive Use":"Defensive Use","Sex crime":"Sex crime",
            "Accidental Shooting":"Accidental Shooting","Child Involved Incident":"Child Involved Incident","Drug involvement":"Drug involvement", "Hate":"Hate crime", "Kidnapping":"Kidnapping/abductions/hostage",
            "Officer shot":"Officer Involved Shooting","ATF/LE":"Confiscation/Raid/Arrest", "School Incident":"School Incident","stolen":"Illegally owned gun(s) recovered during arrest/warrant","Road rage":"Road rage","Gang":"Gang involvement","Possession":"Possession",
            "Shots Fired - No Injuries":"Shots Fired - No Injuries","Car":"Car-jacking","Domestic Violence":"Domestic Violence","Bar":"Bar Fight","Suicide":"Suicide","Officer Involved Shooting":"Officer Involved Shooting",
            "Officer Involved Incident":"Officer Involved Incident","Pistol-whipping":"Pistol-whipping","Non-Aggression Incident":"Accidental Shooting", "Shots fired, no action":"Shots fired, no evidence found","Shot - Wounded/Injured":"Shot - Wounded/Injured",
            "Implied Weapon":"Non-Shooting Incident" }


    search_dict3 = {k.lower(): v for k, v in incident.items()}

    df["incident_characteristics"] = df["incident_characteristics"].map(lambda x: search_dict3.get(next((i for i in search_dict3 if i in str(x).lower()), x), x))
    # Fixing inconsistencies in the df 
    condition4 = df['incident_characteristics'] == "Non-Shooting Incident"
    condition5 = df['n_injured'] > 0
    condition6 = df.notes.str.contains("rob")
    df.loc[condition4 & condition5 & condition6, 'incident_characteristics'] = "Armed robbery"
    
    condition7 = df['incident_characteristics'] == "Shots Fired - No Injuries"
    condition8 = df['n_injured'] > 0

    df.loc[condition7 & condition8, 'incident_characteristics'] = "Shot - Wounded/Injured"
    condition9 = df["incident_characteristics"] == "Illegally owned gun(s) recovered during arrest/warrant"
    df.loc[condition9, 'gun_stolen'] = "Stolen"
    #
    df['age_group'] = df['participant_age_group'].apply(mode_list)

    return df
 


def final_clean(df):
    df.drop(columns=["participant_type","notes","participant_age_group","participant_gender"], inplace=True)
    return df
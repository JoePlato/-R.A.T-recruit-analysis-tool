#adding 3d stuff

import pandas as pd
import random as rd
import numpy as np
from sklearn import linear_model as lm
import scipy.integrate as integrate
import scipy.special as special
import math
from dotenv import load_dotenv
import os

def math_stuff(filePath):
    #read in JMU data
    #
    df = pd.read_csv(r"Assets/JMUFBDATA.csv")
    load_dotenv()
    signifValue = os.getenv("SIGNIFICANCE")
    #set column headers
    cdata = df.columns

    #initialize dataframes
    PsB = pd.DataFrame(columns = cdata)
    #these are JMU hs stats
    PtB = pd.DataFrame(columns = cdata)

    jmudata = df.drop('NAME', axis=1)
    jmudata.columns


    unidrop = ['HHAND', 'HHEIGHT', 'HWEIGHT', 'HWING', 'HVERT', 'HBROAD', 'H401',
        'H402', 'HSHUT']
    hsdrop = ['UHAND', 'UHEIGHT', 'UWEIGHT', 'UWING', 'UVERT',
        'UBROAD', 'U401', 'U 402', 'USHUT']

    jmuhs = jmudata.drop(hsdrop, axis=1)
    jmuhs_names = jmuhs.columns

    jmuuni = jmudata.drop(unidrop, axis=1)
    jmuuni_names = jmuuni.columns

    exp_9tiles = [2.25277, 1.61314, 1.26065, 1.02493, 0.8527, .72035, .6151, .5295, .4587] 
    #    exp_9ntiles = [1'HHAND', 2'HHEIGHT', 3'HWEIGHT', 4'HWING', 5'HVERT', 6'HBROAD', 7'H401', 8'H402', 9'HSHUT']
    #    sP = [9'HHAND', 8'HHEIGHT', 7'HWEIGHT', 6'HWING', 5'HVERT', 4'HBROAD', 1'H401', 2'H402', 3'HSHUT']
    sP = [.4587, .5295, .6151, .72035, 0.8527, 1.02493, 2.25277, 1.61314, 1.26065]
    sP_df_hs = pd.DataFrame(columns=jmuhs_names)
    sP_df_uni = pd.DataFrame(columns=jmuuni_names)

    for i in range(len(jmudata.index)):
        sP_df_hs.loc[i] = sP 
        sP_df_uni.loc[i] = sP


    VBL_hs = pd.DataFrame(columns = ['HS'])
    VBL_uni = pd.DataFrame(columns = ['UNI'])

    #HS player valuation
    for i in range(len(jmuhs.index)):
        for j in range(8):
            a = sP_df_hs.iloc[i]
            if (j == 0) or (j == 1):
                jmuhs.iloc[i,j] = math.exp(-jmuhs.iloc[i,j])
            b = jmuhs.iloc[i]

            VBL_hs.loc[i] = np.dot(a,b)

    #Uni player valuation
    for i in range(len(jmuuni.index)):
        for j in range(8):
            a = sP_df_uni.iloc[i]
            if (j == 0) or (j == 1):
                jmuuni.iloc[i,j] = math.exp(-jmuuni.iloc[i,j])
            b = jmuuni.iloc[i]

            

            VBL_uni.loc[i] = np.dot(a,b)

    uni_max = VBL_uni.max(axis=0)
    hs_max = VBL_hs.max(axis=0)

    for i in range(len(jmudata)):
        VBL_uni.loc[i] = VBL_uni.loc[i]/uni_max
        VBL_hs.loc[i] = VBL_hs.loc[i]/hs_max
    jmu_reg = pd.DataFrame(columns=['HS PV', 'UNI PV'])

    jmu_reg = VBL_hs

    jmu_reg.insert(1, 'UNI', VBL_uni)

    #export to csv then go to R
    exportnum = 1
    #jmu_reg.to_csv(f'JMU Regression Data{exportnum}.csv')

    #linear regression
    x = jmu_reg[['HS']]
    y = jmu_reg[['UNI']]
    LinearRegression = lm.LinearRegression()
    model = LinearRegression.fit(x, y)

    r_sq = model.score(x,y)


    #plot everything
    y_pred = model.predict(x)

    #print(f"R-Squared: {r_sq}")
    #print(f'Yhat = {model.intercept_} + {model.coef_}X')

    #display(VBL_hs)

    recruit_data = pd.read_csv(filePath)
    #name_data = recruit_data[['NAME']]
    recruit_data = recruit_data.drop(['NAME'], axis=1)
    recruit_data = recruit_data.dropna()
    recruitPV = pd.DataFrame(columns=['HS'])
    recruit_sP = pd.DataFrame(columns=unidrop)


    num_rows = recruit_data.shape[0]
    for i in range(num_rows):
        recruit_sP.loc[i] = sP
    
    
    #establishes recruitPV
    for i in range(num_rows):
        for j in range(8):
            a = recruit_sP.iloc[i]
            if (j == 6) or (j == 7):
                recruit_sP.iloc[i,j] = math.exp(-recruit_sP.iloc[i,j])
            b = recruit_data.iloc[i]
            recruitPV.loc[i] = np.dot(a,b)
            recruitPV.loc[i] = recruitPV.loc[i]/hs_max

    #ok now evaluate the regression model with recruit data
    predicted_uni = model.predict(recruitPV)

    jmu_reg_recruits = recruitPV

    jmu_reg_recruits.insert(1, 'UNI', predicted_uni)

    #display(jmu_reg_recruits)

    #now concat the old data and the new recruit data

    ########################
    #CHANGE TO TEST RECRUITS; INDEXED FROM ZERO -> ROW NUMBERS MINUS ONE
    
    ########################
    returnVal = {}
    for recruit in range(num_rows):
        
        choice = jmu_reg_recruits.iloc[recruit]
        
        
        jmu_reg.loc[num_rows]= choice

        x2 = jmu_reg[['HS']]
        y2 = jmu_reg[['UNI']]

        model2 = LinearRegression.fit(x2, y2)

        r_sq2 = model2.score(x2,y2)

        #plot everything


        #print(f"R-Squared: {r_sq2}")
        #print(f'Yhat = {model2.intercept_} + {model2.coef_}X')

        #now compare R-Squared
        significance = r_sq2-r_sq

        #75th quantile for sig

        if significance > signifValue:
            # print('We reject the recruit because they were above the significance threshold.')
            # print(f'The significance of change in the model from the recruit is {significance}.')
            sig_accept = False
        else:
            # print('The recruit is below the significance threshold. (Good)')
            # print(f'The significance of change in the model from the recruit is {significance}.')
            sig_accept = True


        #quantile test

        ########################
        #MIN THRESHOLD
        threshold = jmu_reg.quantile([0.75])
        ########################

        min_threshold = threshold.iloc[0,0]
        a = jmu_reg_recruits.iloc[recruit,0]
        isSucess = False

        print('-----------------------------------------')

        if a < min_threshold:
            # print('We reject the recruit since they are below the third quantile.')
            # print(f'3rd Quantile: {min_threshold}')
            # print(f'Recruit:{a}')
            quant_accept = False
        else:
            # print('Recruit is in the 3rd quantile. (Good)')
            # print(f'3rd Quantile: {min_threshold}')
            # print(f'Recruit:{a}')
            quant_accept = True

        print('-----------------------------------------')
        
        if quant_accept == True and sig_accept == True:
            # print(f"We recommend this recruit with a significance value of {significance} and a quantile significance of {a/min_threshold}.")
            isSucess = True
        # else:
        #     print(f'We reject this recruit with a significance value of {significance} and a quantile significance of {a/min_threshold}.')
        someVal = a/min_threshold
        returnVal[recruit] = [min_threshold,significance,someVal, isSucess]
        print(returnVal[recruit])
    return returnVal

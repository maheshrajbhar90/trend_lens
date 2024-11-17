# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 12:02:39 2024

@author: Mahesh_Kumar
"""

import pandas as pd
import numpy as np
import warnings

# with warnings.catch_warnings():
    # warnings.simplefilter("ignore", FutureWarning)
    # Your code that triggers the FutureWarning
 

class TechnicalAnalysis:
    def __init__(self):   
        pass 

   
    def doji(self, ohlc_df):    
        """returns dataframe with doji candle column"""
        df = ohlc_df.copy()
        avg_candle_size = abs(df["Close"] - df["Open"]).median()
        
        df["doji"] = abs(df["Close"] - df["Open"]) <=  (0.05 * avg_candle_size)
        return df

    
    
    def maru_bozu(self,ohlc_df):   
        
        df = ohlc_df.copy()
        avg_candle_size = abs(df["Close"] - df["Open"]).median()
        df["h-c"] = df["High"] - df["Close"]
        df["l-o"] = df["Low"] - df["Open"]
        df["h-o"] = df["High"] - df["Open"]
        df["l-c"] = df["Low"] - df["Close"]
        
        # Ensure Series have the same index
        df["h-c_l-o_max"] = df[["h-c", "l-o"]].max(axis=1)
        
        # Use element-wise comparison with aligned indices
        maru_bozu_condition = (
        (df["Close"] - df["Open"]).abs() > 2 * avg_candle_size  # Large body size
        ) & (
        df["h-c_l-o_max"] < 0.005 * avg_candle_size  # Minimal shadows
        )
        
        for index, row in df.iterrows():
            if (row['Close'] - row['Open']) > 2 * avg_candle_size and (row['High'] - row['Close']) + (row['Low'] - row['Open']) < 0.01 * avg_candle_size:
                df.loc[index, 'maru_bozu'] = 'maru_bozu_green'
            elif (row['Open'] - row['Close']) > 2 * avg_candle_size and (row['High'] - row['Open']) + (row['Low'] - row['Close']) < 0.01 * avg_candle_size:
                df.loc[index, 'maru_bozu'] = 'maru_bozu_red'
            else:
                df.loc[index, 'maru_bozu'] = False
                
        df.drop(["h-c", "l-o", "h-o", "l-c",'h-c_l-o_max'], axis=1, inplace=True)
        
        return df
        

    def engulfing_pattern(self, ohlc_df):
        """Returns a DataFrame with bullish and bearish engulfing pattern columns."""
        df = ohlc_df.copy()
        
        # Calculate Bullish Engulfing Pattern
        df["bullish_engulfing"] = np.where(
            (df["Close"].shift(1) < df["Open"].shift(1)) &  # Previous day was bearish
            (df["Open"] < df["Close"].shift(1)) &           # Current day's open is below previous day's close
            (df["Close"] > df["Open"].shift(1)) &           # Current day's close is above previous day's open
            (df["Close"] > df["Open"]),                     # Current day is bullish
            True, False
        )
        
        # Calculate Bearish Engulfing Pattern
        df["bearish_engulfing"] = np.where(
            (df["Close"].shift(1) > df["Open"].shift(1)) &  # Previous day was bullish
            (df["Open"] > df["Close"].shift(1)) &           # Current day's open is above previous day's close
            (df["Close"] < df["Open"].shift(1)) &           # Current day's close is below previous day's open
            (df["Close"] < df["Open"]),                     # Current day is bearish
            True, False
        )
        
        return df
    
    def piercing_pattern(self,ohlc_df):
        
        """Returns a DataFrame with a bullish piercing pattern column."""
        df = ohlc_df.copy()
    
        df['piercing_pattern'] = False
    
        for i in range(1, len(df)):
            prev_close = df.loc[i - 1, 'Close']
            prev_open = df.loc[i - 1, 'Open']
            curr_close = df.loc[i, 'Close']
            curr_open = df.loc[i, 'Open']
            prev_low = df.loc[i - 1, 'Low']
    
            if prev_close < prev_open and curr_open < prev_low and curr_close > (prev_close + prev_open) / 2:
                df.loc[i, 'piercing_pattern'] = True
    
        return df
        
    def dark_cloud_cover(self,ohlc_df):
        
        """Returns a DataFrame with a bearish Dark Cloud Cover pattern column."""
        df = ohlc_df.copy()
    
        # Calculate Dark Cloud Cover Pattern
        df["dark_cloud_cover"] = np.where(
            (df["Close"].shift(1) > df["Open"].shift(1)) &  # Previous day was bullish
            (df["Open"] > df["High"].shift(1)) &  # Current day's open is above previous day's high
            (df["Close"] < df["Open"].shift(1)),  # Current day's close is below previous day's open
            True,
            False
        )
    
        return df
    
    def three_black_crows(self,ohlc_df):        
        df = ohlc_df.copy()    
        # Calculate Three Black Crows Pattern
        df["three_black_crows"] = np.where(
        (df["Close"].shift(2) > df["Open"].shift(2)) &  # 3rd previous day was bullish
        (df["Close"] < df["Open"]) &  # Current day is bearish
        (df["Close"].shift(1) < df["Open"].shift(1)) &  # Previous day was bearish
        (df["Open"] < df["Close"].shift(1)) &  # Current day's open is within previous day's body
        (df["Close"] < df["Close"].shift(1)) &  # Current day closes lower than previous day
        (df["Close"].shift(1) < df["Close"].shift(2)),  # Previous day closes lower than 2nd previous day
        True,
        False)
    
        return df


    def three_white_soldiers(self,ohlc_df):
        """Returns a DataFrame with a bullish Three White Soldiers pattern column."""
        df = ohlc_df.copy()
    
        # Calculate Three White Soldiers Pattern
        df["three_white_soldiers"] = np.where(
            (df["Close"].shift(2) < df["Open"].shift(2)) &  # 3rd previous day was bearish
            (df["Close"].shift(1) < df["Open"].shift(1)) &  # 2nd previous day was bearish
            (df["Close"] > df["Open"]) &  # Current day is bullish
            (df["Open"] > df["Close"].shift(1)) &  # Current day gaps up
            (df["Close"] > df["Close"].shift(1)) &  # Current day closes higher than previous day
            (df["Close"].shift(1) > df["Close"].shift(2)),  # Previous day closes higher than 2nd previous day
            True,
            False
        )
    
        return df
       
    def harami_pattern(self,ohlc_df):
        """Returns a DataFrame with Bullish and Bearish Harami pattern columns."""
        df = ohlc_df.copy()
    
        df['bullish_harami'] = False
        df['bearish_harami'] = False
    
        for i in range(1, len(df)):
            prev_close = df.loc[i - 1, 'Close']
            prev_open = df.loc[i - 1, 'Open']
            curr_close = df.loc[i, 'Close']
            curr_open = df.loc[i, 'Open']
    
            # Bullish Harami
            if prev_close < prev_open and curr_close > curr_open and curr_open < prev_close and curr_close > prev_open:
                df.loc[i, 'bullish_harami'] = True
    
            # Bearish Harami
            if prev_close > prev_open and curr_close < curr_open and curr_open > prev_close and curr_close < prev_open:
                df.loc[i, 'bearish_harami'] = True
    
        return df
    
    def tweezer_tops_bottoms(self, ohlc_df):
        """Returns a DataFrame with Tweezer Tops and Tweezer Bottoms pattern columns."""
        df = ohlc_df.copy()

        # Calculate Tweezer Tops
        df["tweezer_tops"] = np.where(
            (df["High"] == df["High"].shift(1)) &           # Current day and previous day have the same high
            (df["Close"] < df["Open"]),                     # Current day is bearish
            True, False
        )

        # Calculate Tweezer Bottoms
        df["tweezer_bottoms"] = np.where(
            (df["Low"] == df["Low"].shift(1)) &             # Current day and previous day have the same low
            (df["Close"] > df["Open"]),                     # Current day is bullish
            True, False
        )

        return df



    def hammer(self,ohlc_df):    
        """returns dataframe with hammer candle column"""
        df = ohlc_df.copy()
        df["hammer"] = (((df["High"] - df["Low"])>3*(df["Open"] - df["Close"])) & \
                        ((df["Close"] - df["Low"])/(.001 + df["High"] - df["Low"]) > 0.6) & \
                        ((df["Open"] - df["Low"])/(.001 + df["High"] - df["Low"]) > 0.6)) & \
                        (abs(df["Close"] - df["Open"]) > 0.1* (df["High"] - df["Low"]))
        return df


    def shooting_star(self,ohlc_df):    
        """returns dataframe with shooting star candle column"""
        df = ohlc_df.copy()
        df["shooting_star"] = (((df["High"] - df["Low"])>3*(df["Open"] - df["Close"])) & \
                        ((df["High"] - df["Close"])/(.001 + df["High"] - df["Low"]) > 0.6) & \
                        ((df["High"] - df["Open"])/(.001 + df["High"] - df["Low"]) > 0.6)) & \
                        (abs(df["Close"] - df["Open"]) > 0.1* (df["High"] - df["Low"]))
        return df
    
    

    def levels(self,ohlc_day):    
        """returns pivot point and support/resistance levels"""
        High = round(ohlc_day["High"].iloc[-1],2)
        Low = round(ohlc_day["Low"].iloc[-1],2)
        Close = round(ohlc_day["Close"].iloc[-1],2)
        pivot = round((High + Low + Close)/3,2)
        r1 = round((2*pivot - Low),2)
        r2 = round((pivot + (High - Low)),2)
        r3 = round((High + 2*(pivot - Low)),2)
        s1 = round((2*pivot - High),2)
        s2 = round((pivot - (High - Low)),2)
        s3 = round((Low - 2*(High - pivot)),2)
        return (pivot,r1,r2,r3,s1,s2,s3)
    
    def calculate_rsi(self,ohlc_df, window=14):
        
        close=ohlc_df['Close'].copy()
        
        delta = close.diff()  # Difference in prices
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        
        # Using exponentially weighted mean to smooth values
        avg_gain = gain.ewm(alpha=1/window, min_periods=window).mean()
        avg_loss = loss.ewm(alpha=1/window, min_periods=window).mean()
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    
    def calculate_vwap(self,ohlc_df):
        df=ohlc_df.copy()
        # df['VWAP'] = (df['Volume'] * (df['High'] + df['Low'] + df['Close']) / 3).cumsum() / df['Volume'].cumsum()
        vwap = (df['Volume'] * (df['High'] + df['Low'] + df['Close']) / 3).cumsum() / df['Volume'].cumsum()

        return vwap

    def trend(self,ohlc_df,n):
        "function to assess the trend by analyzing each candle"
        df = ohlc_df.copy()
        df["up"] = np.where(df["Low"]>=df["Low"].shift(1),1,0)
        df["dn"] = np.where(df["High"]<=df["High"].shift(1),1,0)
        if df["Close"].iloc[-1] > df["Open"].iloc[-1]:
            if df["up"].iloc[-1*n:].sum() >= 0.7*n:
                return "uptrend"
        elif df["Open"].iloc[-1] > df["Close"].iloc[-1]:
            if df["dn"].iloc[-1*n:].sum() >= 0.7*n:
                return "downtrend"
        else:
            return None
 
    def res_sup(self,ohlc_df,ohlc_day):
        """calculates Closest resistance and support levels for a given candle"""
        level = ((ohlc_df["Close"][-1] + ohlc_df["Open"].iloc[-1])/2 + (ohlc_df["High"].iloc[-1] + ohlc_df["Low"].iloc[-1])/2)/2
        p,r1,r2,r3,s1,s2,s3 = self.levels(ohlc_day)
        l_r1=level-r1
        l_r2=level-r2
        l_r3=level-r3
        l_p=level-p
        l_s1=level-s1
        l_s2=level-s2
        l_s3=level-s3
        lev_ser = pd.Series([l_p,l_r1,l_r2,l_r3,l_s1,l_s2,l_s3],index=["p","r1","r2","r3","s1","s2","s3"])
        sup = lev_ser[lev_ser>0].idxmin()
        res = lev_ser[lev_ser<0].idxmax()
        return (eval('{}'.format(res)), eval('{}'.format(sup)))

    def candle_type(self,ohlc_df):    
        """returns the candle type of the last candle of an OHLC DF"""
        candle = None
        if self.doji(ohlc_df)["doji"].iloc[-1] == True:
            candle = "doji"    
        if self.maru_bozu(ohlc_df)["maru_bozu"].iloc[-1] == "maru_bozu_green":
            candle = "maru_bozu_green"       
        if self.maru_bozu(ohlc_df)["maru_bozu"].iloc[-1] == "maru_bozu_red":
            candle = "maru_bozu_red"        
        if self.shooting_star(ohlc_df)["shooting_star"].iloc[-1] == True:
            candle = "shooting_star"        
        if self.hammer(ohlc_df)["hammer"].iloc[-1] == True:
            candle = "hammer"  
        if self.engulfing_pattern(ohlc_df)['bullish_engulfing'].iloc[-1]==True:
            candle="Bullish_engulfing"
        if self.engulfing_pattern(ohlc_df)['bearish_engulfing'].iloc[-1]==True:
            candle="Bearish_engulfing"
         
            
        if self.three_white_soldiers(ohlc_df)['three_white_soldiers'].iloc[-1]==True:
            candle="Three_white_soldiers"
        if self.three_black_crows(ohlc_df)['three_black_crows'].iloc[-1]==True:
            candle="three_black_crows"
        if self.dark_cloud_cover(ohlc_df)['dark_cloud_cover'].iloc[-1]==True:
            candle="dark_cloud_cover"
        if self.piercing_pattern(ohlc_df)['piercing_pattern'].iloc[-1]==True:
            candle="piercing_pattern"
        if self.harami_pattern(ohlc_df)['bullish_harami'].iloc[-1]==True:
            candle="bullish_harami"
        if self.harami_pattern(ohlc_df)['bearish_harami'].iloc[-1]==True:
            candle="bearish_harami"    
        if self.tweezer_tops_bottoms(ohlc_df)['tweezer_tops'].iloc[-1]==True:
            candle='tweezer_tops'
        if self.tweezer_tops_bottoms(ohlc_df)['tweezer_bottoms'].iloc[-1]==True:
            candle='tweezer_bottoms'
            
        return candle
    
    

    def candle_pattern(self,ohlc_df,ohlc_day):    
        """returns the candle pattern identified"""
        pattern = None
        signi = "Low"
        avg_candle_size = abs(ohlc_df["Close"] - ohlc_df["Open"]).median()
        sup, res = self.res_sup(ohlc_df,ohlc_day)

        if (sup - 1.5*avg_candle_size) < ohlc_df["Close"].iloc[-1] < (sup + 1.5*avg_candle_size):
            signi = "High"

        if (res - 1.5*avg_candle_size) < ohlc_df["Close"].iloc[-1] < (res + 1.5*avg_candle_size):
            signi = "High"

        if self.candle_type(ohlc_df) == 'doji' \
            and ohlc_df["Close"].iloc[-1] > ohlc_df["Close"].iloc[-2] \
            and ohlc_df["Close"].iloc[-1] > ohlc_df["Open"].iloc[-1]:
                pattern = "doji_bullish"

        if self.candle_type(ohlc_df) == 'doji' \
            and ohlc_df["Close"].iloc[-1] < ohlc_df["Close"].iloc[-2] \
            and ohlc_df["Close"].iloc[-1] < ohlc_df["Open"].iloc[-1]:
                pattern = "doji_bearish" 

        if self.candle_type(ohlc_df) == "maru_bozu_green":
            pattern = "maru_bozu_bullish"

        if self.candle_type(ohlc_df) == "maru_bozu_red":
            pattern = "maru_bozu_bearish"

        if self.trend(ohlc_df.iloc[:-1,:],7) == "uptrend" and self.candle_type(ohlc_df) == "hammer":
            pattern = "hanging_man_bearish"

        if self.trend(ohlc_df.iloc[:-1,:],7) == "downtrend" and self.candle_type(ohlc_df) == "hammer":
            pattern = "hammer_bullish"

        if self.trend(ohlc_df.iloc[:-1,:],7) == "uptrend" and self.candle_type(ohlc_df) == "shooting_star":
            pattern = "shooting_star_bearish"

        if self.trend(ohlc_df.iloc[:-1,:],7) == "uptrend" \
            and self.candle_type(ohlc_df) == "doji" \
            and ohlc_df["High"].iloc[-1] < ohlc_df["Close"].iloc[-2] \
            and ohlc_df["Low"].iloc[-1] > ohlc_df["Open"].iloc[-2]:
            pattern = "harami_cross_bearish"

        if self.trend(ohlc_df.iloc[:-1,:],7) == "downtrend" \
            and self.candle_type(ohlc_df) == "doji" \
            and ohlc_df["High"].iloc[-1] < ohlc_df["Open"].iloc[-2] \
            and ohlc_df["Low"].iloc[-1] > ohlc_df["Close"].iloc[-2]:
            pattern = "harami_cross_bullish"

        if self.trend(ohlc_df.iloc[:-1,:],7) == "uptrend" \
            and self.candle_type(ohlc_df) != "doji" \
            and ohlc_df["Open"].iloc[-1] > ohlc_df["High"].iloc[-2] \
            and ohlc_df["Close"].iloc[-1] < ohlc_df["Low"].iloc[-2]:
            pattern = "engulfing_bearish"

        if self.trend(ohlc_df.iloc[:-1,:],7) == "downtrend" \
            and self.candle_type(ohlc_df) != "doji" \
            and ohlc_df["Close"].iloc[-1] > ohlc_df["High"].iloc[-2] \
            and ohlc_df["Open"].iloc[-1] < ohlc_df["Low"].iloc[-2]:
            pattern = "engulfing_bullish"
            
        if self.candle_type(ohlc_df) == "Bullish_engulfing":
            pattern = "bullish_engulfing"

        if self.candle_type(ohlc_df) == "Bearish_engulfing":
            pattern = "bearish_engulfing"
            
        if self.candle_type(ohlc_df) == "Three_white_soldiers":
            pattern = "three_white_soldiers"
            
        if self.candle_type(ohlc_df) == "three_black_crows":
            pattern = "three_black_crows"
            
        if self.candle_type(ohlc_df) == "dark_cloud_cover":
            pattern = "dark_cloud_cover"
            
        if self.candle_type(ohlc_df) == "piercing_pattern":
            pattern = "piercing_pattern"
            
        if self.candle_type(ohlc_df) == "bullish_harami":
            pattern = "bullish_harami"
            
        if self.candle_type(ohlc_df) == "bearish_harami":
            pattern = "bearish_harami"
            
        if self.candle_type(ohlc_df) == "tweezer_tops":
            pattern = "tweezer_tops"
            
        if self.candle_type(ohlc_df) == "tweezer_bottoms":
            pattern = "tweezer_bottoms"    
                    

        return "Significance - {}, Pattern - {}".format(signi,pattern)
    

    
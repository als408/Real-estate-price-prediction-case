import unittest,sys
from pathlib import Path
import numpy as np
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from pricepred.workflow import parse_params,clean_text,shared_split,prepare_features,merge_llm

class WorkflowTests(unittest.TestCase):
 def test_separator_and_price_removal(self):
  self.assertEqual(parse_params('price<=>500000<br>price[currency]<=>PLN<br>price_per_m<=>10000<br>m<=>50<br>building_type<=>block'),{'m':'50','building_type':'block'})
 def test_mask_preserves_nonmonetary_numbers(self):
  text=clean_text('<p>500 000 zł, 3 pokoje, 50 m2 &amp; balkon</p>')
  self.assertNotIn('500',text);self.assertIn('3 pokoje',text);self.assertIn('50 m2',text);self.assertIn('&',text)
 def test_split_whole_day_and_duplicate_id(self):
  data=pd.DataFrame({'id':[1,2,3,4,5,5], 'market':['secondary']*6,
    'created_at_first':['2020-01-01','2020-01-02','2020-01-03','2020-01-04','2020-01-05','2020-01-05'],
    'created_at':['2020-01-06']*6,'price':[1,2,3,4,5,5]})
  df,tr,te,cut=shared_split(data)
  self.assertEqual(len(df),5);self.assertEqual(set(df.loc[te,'id']),{5})
  self.assertLess(df.loc[tr,'published_at'].max(),df.loc[te,'published_at'].min())
 def test_cached_real_data_integrity(self):
  root=Path(__file__).resolve().parents[1]
  frame,tr,te,_=shared_split(pd.read_csv(root/'data/real_estate_ads.csv'))
  prepared=prepare_features(frame)
  self.assertTrue(prepared.index.equals(frame.index));self.assertEqual((len(tr),len(te)),(4758,1196))
  self.assertTrue(prepared.loc[prepared['m_raw'].eq(267000),'m'].isna().all())
  llm=pd.read_csv(root/'llm_features_new.csv');merged=merge_llm(prepared,llm)
  self.assertTrue(merged.index.equals(frame.index))
  with self.assertRaises(ValueError):merge_llm(prepared,pd.concat([llm,llm.iloc[:1]]))
if __name__=='__main__':unittest.main()

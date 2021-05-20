// Find the effective entries in the Run 1 MC templates
// and compare them to the fitted yields.
// Needs the templates from
// https://gitlab.cern.ch/bhamilto/rdvsrdst-histfactory/-/blob/master/proctuples/BCandHistos_D0.root
// https://gitlab.cern.ch/bhamilto/rdvsrdst-histfactory/-/blob/master/proctuples/BCandHistos_Dst.root

#include <sstream>
#include <ostream>
#include <iostream>
#include <iomanip>
#include <vector>
#include "TString.h"
#include "TObject.h"
#include "TH3D.h"
#include "TKey.h"
#include "TFile.h"

using namespace std;

TString RoundNumber(double num, int decimals, double denom=1.){
  if(denom==0 || !isfinite(num) || !isfinite(denom)) return " - ";
  double neg = 1; if(num*denom<0) neg = -1;
  num /= neg*denom; num += 0.5*pow(10.,-decimals);
  if(abs(num) > 1e16) return "-";
  long num_int = static_cast<long>(num);
  long num_dec = static_cast<long>((1+num-num_int)*pow(10.,decimals));
  TString s_dec = ""; s_dec += num_dec; s_dec.Remove(0,1);
  TString result="";
  if(neg<0) result+="-";
  result+= num_int;
  if(decimals>0) {
    result+="."; result+=s_dec;
  }

  TString afterdot = result;
  afterdot.Remove(0,afterdot.First(".")+1);
  for(int i=0; i<decimals-afterdot.Length(); i++)
    result += "0";
  if(result.Length()>15) cout<<"num "<<num<<", denom "<<denom<<"  ---->  "<<result<<endl;
  return result;
}

TString AddCommas(double num, int decimals){
  TString result = RoundNumber(num, decimals);
  int posdot(result.First('.'));
  if(posdot==-1) posdot = result.Length();
  for(int ind(posdot-3); ind > 0; ind -= 3)
    result.Insert(ind, ",");

  return result;
}


void doTable(TString filename, vector<TString> names, vector<double>  yields){
  TFile *infile = new TFile(filename);

  cout<<endl<<"Doing "<<filename<<endl<<"==============================================="<<endl;
  for(unsigned ind=0; ind<names.size(); ind++){
    TString hname = "h_" + names[ind];
    for (TObject* keyAsObj : *infile->GetListOfKeys()){
      auto key = dynamic_cast<TKey*>(keyAsObj);
      TString name = key->GetName();

      if(name != hname) continue;
      TObject* obj = key->ReadObj();
      if (!obj->IsA()->InheritsFrom("TH3D")) continue;
      TH3D* h= (TH3D*)obj;
      double neff = h->GetEffectiveEntries(), ntot = h->GetEntries();
      for(int i=0; i<9720; i++){
        if(h->GetBinContent(i)<1e-9) ntot--;
      } // Phoebe fills bins with no MC events with small weight, which increases the number of entries
      cout<<setw(13)<<name<<":   "<<setw(9)<<AddCommas(neff,0)<<" / "<<setw(9)<<AddCommas(ntot,0)<<" = "<<setw(5)<<RoundNumber(100*neff/ntot,1)<<"%     MC/data = "<<setw(5)<<RoundNumber(neff/yields[ind],1)<<"   (data = "<<setw(7)<<AddCommas(yields[ind],0)<<")"<<endl;
    }
  }

  cout<<endl;
}

void listNames(TString filename){
  TFile *infile = new TFile(filename);
  cout<<endl<<"Doing "<<filename<<endl<<"==============================================="<<endl;
  for (TObject* keyAsObj : *infile->GetListOfKeys()){
    auto key = dynamic_cast<TKey*>(keyAsObj);
    TString name = key->GetName();
    if(name.Contains("_res")) continue;
    if(name.Contains("DOCA")) continue;
    if(name.Contains("misID")) continue;
    if(name.Contains("comb")) continue;
    
    //if(!name.Contains("pipi") ) continue;
    //if(!name.Contains("tau") ) continue;
    if(!name.Contains("ALT") ) continue;
    cout<<name<<endl;
  }
  cout<<endl;
}

void yields_MC(){

  //listNames("proctuples_BCandHistos_D0.root");
  //listNames("proctuples_BCandHistos_Dst.root");
  //return;

  double RDss = 0.12 * 0.7 * 0.1741; // RD** * eff_sig/eff_norm * BF(tau -> mu nu) 
  vector<TString> D0names({"Dmu_ALT", "uDstmuALT", "dDstmuALT", "dD0muALT", "uD0muALT", "dD1muALT", "uD1muALT", "dD1pmuALT", "uD1pmuALT", "dD2muALT", "uD2muALT", "dD0tauALT", "uD0tauALT", "dD1tauALT", "uD1tauALT", "dD1ptauALT", "uD1ptauALT", "dD2tauALT", "uD2tauALT","Dpipimu", "Dstzpipimu", "Dstppipimu","sDs1pmuALT","sDs2muALT", "uDDmu","dDDmu","uDDtau","dDDtau"});
  vector<double>   D0Greg({3.66e5,    9.17e5,      6.95e4,      9.56e3,     2.02e4,     3.66e3 ,    4.8e4,      8.15e3,      7.38e3,      5.2e3,      1.63e3,     1.74e3,      1.74e3,      1.74e3,      1.74e3,       1.74e3,       1.74e3,      1.74e3,      1.74e3,     3.82e4,     1.24e4,       3.59e3,      7.03e3,      4.2e3   ,    7.49e4, 7.49e4, 4.55e3,  4.55e3});
  vector<double> D0Phoebe({358214,    944864,      71361.9,     4802.21,    6731.07,    13900.6,    29325.1,    6473.94,     7887.02,     3900.77,    5041.93,  4802.21*RDss,  6731.07*RDss, 13900.6*RDss,  29325.1*RDss,  6473.94*RDss,  7887.02*RDss,  3900.77*RDss,5041.93*RDss,1511.04,   49462.2,       4465.13,     4228.45,     1343.69,     38330.7,31483.9, 4845.04, 1003.54}); 
  doTable("BCandHistos_D0.root", D0names, D0Phoebe);
  
  vector<TString> Dstnames({"sigmuALT", "D1_ALT", "D1p_ALT", "D2_ALT", "D1tau_ALT", "D1ptau_ALT", "D2tau_ALT", "D2Smu", "uDDmu", "dDDmu", "dDDtau", "uDDtau"});
  vector<double>   DstGreg({3.31e5,     1.12e4,  1.36e4,    3.22e3,    459,         459,          459,         1,       2.43e4,  2.43e4,  1.08e3,   1.08e3});
  vector<double> DstPhoebe({323024,      8129.17, 8469.96,   2063.15,   8129*RDss,    8469.96*RDss,  2063*RDss,    7521.18, 3805.92, 17633.6, 103.695,  991.056});
  doTable("BCandHistos_Dst.root", Dstnames, DstPhoebe);

  
  
}


  
// {"12573010", "12573012", "B- -> D0 mu nu",                  "Dmu_ALT",          
// {"11574020", "11574021", "B0 -> D*+ mu nu",                 "dDstmuALT",           
// {"12573031", "12773410", "B- -> D*0 mu nu",                 "uDstmuALT",          
// {"12573000", "12573001", "B- -> D0 tau nu",                 "",         
// {"11574010", "11574011", "B0 -> D*+ tau nu",                "",           
// {"12573021", "12773400", "B- -> D*0 tau nu",                "",           
// {"11873010", "11874430", "B0 -> D**+ mu nu",                  
// {"11873030", "11874440", "B0 -> D**+ tau nu",                      
// {"12873010", "12873450", "B- -> D**0 mu nu",                       
// {"12873030", "12873460", "B- -> D**0 tau nu",                      
// {"12675010", "12675011", "B- -> D**(->D0 pi pi) mu nu",      
// {"11674400", "11674401", "B0 -> D**(->D0 pi pi) mu nu",      
// {"12675400", "12675402", "B- -> D**(->D*+ pi pi) mu nu",     
// {"11676010", "11676012", "B0 -> D**(->D*+ pi pi) mu nu",     
// {"12675430", "12875440", "B- -> D**(->D*0 pi pi) mu nu",     
// {"13873000", "13874020", "Bs -> Ds**(->D0K) mu nu",          
// {"13874000", "13674000", "Bs -> D**+mu nu",                  
// {"11873000", "11894600", "B0 -> D0(Xc ->  mu nuX')X",        
// {"11873020", "11894200", "B0 -> D0(Ds -> taunu)X",           
// {"12873000", "12896300", "B+ -> D0(Xc ->  mu nuX')X",        
// {"12873021", "12896310", "B+ -> D0(Ds -> taunu)X",           
// {"11874050", "11894610", "B0 -> D*+ (Xc -> mu nu X')X",      
// {"11874070", "11894210", "B0 -> D*+(Ds -> tau nu) X",        
// {"12874010", "12895400", "B+ -> D*+ (Xc -> mu nu X')X",      
// {"12874030", "12895000", "B+ -> D*+(Ds -> tau nu) X",            


















































from selection.finder import finder as sfnd

#------------------------------------
def get_cuts():
  d_cut = {
    "nspd": "nSPDHits < 450",
    "MTOS": "( ((L1_L0MuonDecision_TOS && L1_PT > 800) || (L2_L0MuonDecision_TOS && L2_PT > 800)) && L0Data_Muon1_Pt >= threshold_mu)",
    "hlt1": "((L1_Hlt1TrackMVADecision_TOS && ( TMath::Log(L1_IPCHI2_OWNPV)  > (1.0/TMath::Power(0.001*L1_PT-1., 2))  + (threshold_b/25000)*(25000-L1_PT) + TMath::Log(7.4) )) || (L2_Hlt1TrackMVADecision_TOS && ( TMath::Log(L2_IPCHI2_OWNPV)  > (1.0/TMath::Power(0.001*L2_PT-1., 2))  + (threshold_b/25000)*(25000-L2_PT) + TMath::Log(7.4) )) || (H_Hlt1TrackMVADecision_TOS && ( TMath::Log(H_IPCHI2_OWNPV)  > (1.0/TMath::Power(0.001*H_PT-1., 2))  + (threshold_b/25000)*(25000-H_PT) + TMath::Log(7.4) )))",
    "hlt2": "(B_Hlt2Topo2BodyDecision_TOS     || B_Hlt2Topo3BodyDecision_TOS     || B_Hlt2TopoMu2BodyDecision_TOS     || B_Hlt2TopoMu3BodyDecision_TOS || B_Hlt2TopoMuMu2BodyDecision_TOS || B_Hlt2TopoMuMu3BodyDecision_TOS)",
    "kinematics": "L1_PT > 800 && L2_PT > 800",
    "cascade": "kl_M_l2pi > 1885 && kl >1885",
    "ghost": "L1_TRACK_GhostProb <0.3 && L2_TRACK_GhostProb<0.3",
    "rich": "L1_hasRich == 1 && L2_hasRich == 1 && H_hasRich == 1",
    "acceptance": "L1_InMuonAcc == 1 && L2_InMuonAcc == 1",
    "jpsi_misid": "abs(kl_M_k2l -  3097.) > 60 && abs(kl_M_k2l -  3686.) > 60",
    "bdt": "BDT_cmb > 0.831497 && BDT_prc > 0.480751",
    "mass": "(B_M                     > 5180) && (B_M                     < 5600)"
  }

  return d_cut
#------------------------------------
def test_simple():
    d_cut = get_cuts()

    obj=sfnd('MTOS', 'high', '2017')
    #obj=sfnd('MTOS', 'jpsi', '2017')
    ver=obj.get_version(d_cut)
#------------------------------------
if __name__ == '__main__':
    test_simple()


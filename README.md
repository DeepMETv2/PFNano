# PFNano

**Warning: instructions for NanoAODv10 are currently tested for 2022 Run3 data only, using `PFnano_customizeData_add_DeepJet`**

This is a [NanoAOD](https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookNanoAOD) framework for advance developments of jet algorithms. 
The current full content of this development branch can be seen [ToDo](http://algomez.web.cern.ch/algomez/testWeb/PFnano_content_v02.html) and the size [ToDo](http://algomez.web.cern.ch/algomez/testWeb/PFnano_size_v02.html).
In this version, PFcandidates can be saved for AK4 only, AK8 only, or all the PF candidates. More below.
This format can be used with [fastjet](http://fastjet.fr) directly.

## Recipe

**THIS IS A DEVELOPMENT BRANCH**

Note that instructions related to different years / campaigns will need to be updated at a later time.


ToDo: rewrite for v10 ... For **UL** 2016, 2017 and 2018 data and MC **NanoAODv8** according to the [XPOG](https://gitlab.cern.ch/cms-nanoAOD/nanoaod-doc/-/wikis/Releases/NanoAODv8) and [PPD](https://twiki.cern.ch/twiki/bin/view/CMS/PdmVRun2LegacyAnalysisSummaryTable) recommendations:

```
cmsrel  CMSSW_12_4_8
cd  CMSSW_12_4_8/src
cmsenv
git clone https://github.com/cms-jet/PFNano.git PhysicsTools/PFNano
git fetch
git switch 12_4_8
scram b -j 10
cd PhysicsTools/PFNano/test
```
Note: When running over a new dataset you should check with [the nanoAOD workbook twiki](https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookNanoAOD#Running_on_various_datasets_from) to see if the era modifiers in the CRAB configuration files are correct. The jet correction versions are taken from the global tag.

## Local Usage:

There are python config files ready to run in `PhysicsTools/PFNano/test/`. Examples to include or exclude the input features for the DeepJet tagger are given in `nano_data_2022_NANO.py`. The list of options that are currently implemented inside `pfnano_cff.py` (e.g. for MC) looks like that:
```
process = PFnano_customizeMC(process)
#process = PFnano_customizeMC_add_DeepJet(process)                  ##### DeepJet inputs are added to the Jet collection
#process = PFnano_customizeMC_add_DeepJet_and_Truth(process)        ##### DeepJet inputs as well as a truth branch with fine-grained labels
#process = PFnano_customizeMC_allPF(process)                        ##### PFcands will contain ALL the PF Cands
#process = PFnano_customizeMC_allPF_add_DeepJet(process)            ##### PFcands will contain ALL the PF Cands; + DeepJet inputs for Jets
#process = PFnano_customizeMC_AK4JetsOnly(process)                  ##### PFcands will contain only the AK4 jets PF cands
#process = PFnano_customizeMC_AK4JetsOnly_add_DeepJet(process)      ##### PFcands will contain only the AK4 jets PF cands; + DeepJet inputs for Jets
#process = PFnano_customizeMC_AK8JetsOnly(process)                  ##### PFcands will contain only the AK8 jets PF cands
#process = PFnano_customizeMC_noInputs(process)                     ##### No PFcands but all the other content is available.
```
In general, whenever `_add_DeepJet` is specified (does not apply to `AK8JetsOnly` and `noInputs`), the DeepJet inputs are added to the Jet collection. For all other cases that involve adding tagger inputs, only DeepCSV and / or DDX are taken into account as default (= the old behaviour when `keepInputs=True`). Internally, this is handled by selecting a list of taggers, namely choosing from `DeepCSV`, `DeepJet`, and `DDX` (or an empty list for the `noInputs`-case, formerly done by setting `keepInputs=False`, now set `keepInputs=[]`). This refers to a change of the logic inside `pfnano_cff.py` and `addBTV.py`. If one wants to use this new flexibility, one can also define new customization functions with other combinations of taggers. Currently, there are all configurations to reproduce the ones that were available previously, and all configuations that extend the old ones by adding DeepJet inputs. DeepJet outputs, on top of the discriminators already present in NanoAOD, are added in any case where AK4Jets are added, i.e. there is no need to require the full set of inputs to get the individual output nodes / probabilities. The updated description using `PFnano_customizeMC_add_DeepJet` can be viewed here: [ToDo](https://annika-stein.web.cern.ch/PFNano/AddDeepJetTagInfo_desc.html) and the size [ToDo](https://annika-stein.web.cern.ch/PFNano/AddDeepJetTagInfo_size.html).

### How to create python files using cmsDriver

All python config files were produced with `cmsDriver.py`.

Two imporant parameters that one needs to verify in the central nanoAOD documentation are `--conditions` and `--era`. 
- `--era` options from [WorkBookNanoAOD](https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookNanoAOD) or [XPOG](https://gitlab.cern.ch/cms-nanoAOD/nanoaod-doc/-/wikis/Releases/NanoAODv8) and ToDo for Run3!
- `--conditions` can be found here [PdMV](https://twiki.cern.ch/twiki/bin/view/CMS/PdmV)

**Work in progress for Run3, the following .sh are all outdated**

Pre UL `cmsRun` python config files are generated by running `make_configs_preUL.sh`

```
bash make_configs_preUL.sh  # run to only produce configs
bash make_configs_preUL.sh  -e # run to actually execute configs on 1000 events
```

**UL `cmsRun` python config files are generated by running `make_configs_UL.sh`**

```
bash make_configs_UL.sh  # run to only produce configs
bash make_configs_UL.sh  -e # run to actually execute configs on 1000 events
```

## Submission to CRAB

For crab submission a handler script `crabby.py`, a crab baseline template `template_crab.py` and an example 
submission yaml card `card_example_data.yml` are provided.

- A single campaign (data/mc, year, config, output path) should be configured statically in a copy of `card_example_data.yml`.
- To submit:
  ```
  source /cvmfs/grid.cern.ch/centos7-umd4-ui-4_200423/etc/profile.d/setup-c7-ui-example.sh
  source /cvmfs/cms.cern.ch/common/crab-setup.sh prod # note: this is new w.r.t. 106X instructions
  source /cvmfs/cms.cern.ch/cmsset_default.sh
  voms-proxy-init --voms cms --valid 192:00
  cd  CMSSW_12_4_8/src
  cmsenv
  cd PhysicsTools/PFNano/test
  python3 crabby.py -c card_example_data.yml --make --submit
  ```
- `--make` and `--submit` calls are independent, allowing manual inspection of submit configs
- Add `--test True` to disable publication on otherwise publishable config and produce a single file per dataset


## Processing data

When processing data, a lumi mask should be applied. The so called golden JSON should be applicable in most cases. Should also be checked here https://twiki.cern.ch/twiki/bin/view/CMS/PdmV

 * Golden JSON, UL
 
2022 ToDo
```
# 2017: /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/Legacy_2017/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt
# 2018: /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/Legacy_2018/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt
#
```

 * Golden JSON, pre-UL
 
2022 ToDo
```
# 2016
jsons/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt
# 2017 
jsons/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON_v1.txt
# 2018
jsons/Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt
```

Include in `card.yml` for `crabby.py` submission. (In deprecated interactive submissiong add `--lumiMask jsons/...txt`)


## How to create website with nanoAOD content

To create nice websites like [this one](http://algomez.web.cern.ch/algomez/testWeb/JMECustomNano102x_mc_v01.html#Jet) with the content of nanoAOD, use the `inspectNanoFile.py` file from the `PhysicsTools/nanoAOD` package as:
```
python PhysicsTools/NanoAOD/test/inspectNanoFile.py NANOAOD.root -s website_with_collectionsize.html -d website_with_collectiondescription.html
```

## Documenting the Extended NanoAOD Samples

Please document the input and output datasets on the following twiki: https://twiki.cern.ch/twiki/bin/view/CMS/JetMET/JMARNanoAODv1. For the MC, the number of events can be found by looking up the output dataset in DAS. For the data, you will need to run brilcalc to get the total luminosity of the dataset. See the instructions below. 


## Running brilcalc
These are condensed instructions from the lumi POG TWiki (https://twiki.cern.ch/twiki/bin/view/CMS/TWikiLUM). Also see the brilcalc quickstart guide: https://twiki.cern.ch/twiki/bin/viewauth/CMS/BrilcalcQuickStart.

Note: brilcalc should be run on lxplus. It does not work on the lpc.

Instructions:

1.) Add the following lines to your .bashrc file (or equivalent for your shell). Don't forget to source this file afterwards!

    export PATH=$HOME/.local/bin:/cvmfs/cms-bril.cern.ch/brilconda/bin:$PATH
    export PATH=/afs/cern.ch/cms/lumi/brilconda-1.1.7/bin:$HOME/.local/bin:$PATH
    
2.) Install brilws:

    pip install --install-option="--prefix=$HOME/.local" brilws
    
3.) Get the json file for your output dataset. In the area in which you submitted your jobs:

    crab report -d [your crab directory]
    
The processedLumis.json file will tell you which lumi sections you successfully ran over. The lumi sections for incomplete, failed, or unpublished jobs are listed in notFinishedLumis.json, failedLumis.json, and notPublishedLumis.json. More info can be found at https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRAB3Commands#crab_report.
    
4.) Run brilcalc on lxplus:

    brilcalc lumi -i processedLumis.json -u /fb --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json -b "STABLE BEAMS"
    
The luminosity of interest will be listed under "totrecorded(/fb)." You can also run this over the other previously mentioned json files.
    
Note: '-b "STABLE BEAMS"' is optional if you've already run over the golden json. 
        Using the normtag is NOT OPTIONAL, as it defines the final calibrations and detectors that are used for a given run.

# pharmD project : therapeutic repurposing 

This experimental section aims to introduce an initial pipeline for virtual screening, relying exclusively on publicly available database information, as well as prediction algorithms for biological activity parameters and toxicity.

I decided to find molecular entities actives against MET receptor, a commonly mutated tyrosine kinase receptor (TKR) in cancers, outline in Figure 1.

![Figure 1 outline of PharmD practical section](https://github.com/pawlakG/pharmD/blob/f141e3fb89491a4eb6d30d92290f41df89e236b8/output/img/pharmD_Outline.png | width=50)


## Objectives
Deploy a repository workflow example following these steps :
* Get all molecules for a specified indication
* get all physical, biological and pharmacological properties
* Extract shared characteristics
* Search molucules with similar properties
* Remoce already tested molecules
* Remove molecules with too many adverse effects

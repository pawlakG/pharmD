# PharmD project : therapeutic repurposing 

This experimental section aims to introduce an initial pipeline for virtual screening, relying exclusively on publicly available database information, as well as prediction algorithms for biological activity parameters and toxicity.

I decided to find molecular entities actives against MET receptor, a commonly mutated tyrosine kinase receptor (TKR) in cancers, outline in Figure 1.

## Main steps

The first step involves retrieving all active compounds targeting the MET receptor from the ChEMBL database, along with their physicochemical properties and pIC50 values. Among these compounds, only those adhering to Lipinski's rules will be retained (molecular weight below 500 g/mol, fewer than 5 hydrogen bond donors, fewer than 10 hydrogen bond acceptors, and a logP below 5), as well as those devoid of structural motifs associated with undesirable characteristics, such as nitro groups (mutagenic), sulfates and phosphates (likely to confer unfavorable pharmacokinetic properties), 2-halopyridines, and thiols (reactive). Additionally, compounds containing substructures prone to nonspecific binding will be excluded. These analyses were performed using the RDKit Python module.

To increase the number of molecules for screening, we searched for compounds structurally similar to this subset by querying the PubChem database using its REST-based PUG web service. The obtained molecules were subsequently filtered according to the same criteria as the initial set, including physicochemical properties, undesirable substructures, and PAINS (Pan-Assay Interference Compounds).

We predicted the pIC50 of the newly obtained molecules by training a deep learning neural network model with two hidden layers of 64 and 32 neurons, using the ReLU activation function. The model was trained on the initial dataset, leveraging molecular signatures, with the Scikit-Learn Python module. The molecules were subsequently filtered based on their predicted pIC50 values, retaining only those with a pIC50 greater than 9. Finally, toxicity prediction for the retained compounds (both the initial set and the structurally similar molecules) was performed using the eToxPred algorithm. According to Pu et al., a toxicity prediction threshold of 0.58 best discriminates between highly toxic and less toxic compounds. Therefore, only compounds with a toxicity prediction value below 0.58 were retained."

<p align="center"> 
  <img src="https://github.com/pawlakG/pharmD/blob/f141e3fb89491a4eb6d30d92290f41df89e236b8/output/img/pharmD_Outline.png" width=40% height=40%>
  <em>Figure 1: PharmD practical project outline.</em>
</p>

## Active compound on MET, similar compounds and filtering

Following the search for compounds active on the MET receptor, 4,206 IC50 assays were retrieved for 3,204 molecules, with pIC50 values ranging from 3.585 to 9.88 and an average value of 7.25 (Figure 2).

<p align="center"> 
  <img src="https://github.com/pawlakG/pharmD/blob/8e526862e84ebb55294353f952da5fcc67169a07/output/img/activMolMET.png" width=40% height=40%>
  <em>Figure 2: IC50 histogram of MET active compounds.</em>
</p>

After filtering based on Lipinski's rules, as well as removing over-interacting substructures and undesirable structural motifs, 1,308 molecules were selected (Figure 3).

<p align="center"> 
  <img src="https://github.com/pawlakG/pharmD/blob/8e526862e84ebb55294353f952da5fcc67169a07/output/06_similarCompoundMolecularFiltering/simCompoundFiltered.png" width=40% height=40%>
  <em>Figure 3: Radar plot representig globel Lipinski indicators for selected compounds.</em>
</p>



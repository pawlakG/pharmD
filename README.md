# PharmD project : therapeutic repurposing 

This experimental section aims to introduce an initial pipeline for virtual screening, relying exclusively on publicly available database information, as well as prediction algorithms for biological activity parameters and toxicity.

I decided to find molecular entities actives against MET receptor, a commonly mutated tyrosine kinase receptor (TKR) in cancers, outline in Figure 1.

## Main steps

The first step involves retrieving all active compounds targeting the MET receptor from the ChEMBL database, along with their physicochemical properties and pIC50 values. Among these compounds, only those adhering to Lipinski's rules will be retained (molecular weight below 500 g/mol, fewer than 5 hydrogen bond donors, fewer than 10 hydrogen bond acceptors, and a logP below 5), as well as those devoid of structural motifs associated with undesirable characteristics, such as nitro groups (mutagenic), sulfates and phosphates (likely to confer unfavorable pharmacokinetic properties), 2-halopyridines, and thiols (reactive). Additionally, compounds containing substructures prone to nonspecific binding will be excluded. These analyses were performed using the RDKit Python module.

To increase the number of molecules for screening, we searched for compounds structurally similar to this subset by querying the PubChem database using its REST-based PUG web service. The obtained molecules were subsequently filtered according to the same criteria as the initial set, including physicochemical properties, undesirable substructures, and PAINS (Pan-Assay Interference Compounds).

We predicted the pIC50 of the newly obtained molecules by training a deep learning neural network model with two hidden layers of 64 and 32 neurons, using the ReLU activation function. The model was trained on the initial dataset, leveraging molecular signatures, with the Scikit-Learn Python module. The molecules were subsequently filtered based on their predicted pIC50 values, retaining only those with a pIC50 greater than 9. Finally, toxicity prediction for the retained compounds (both the initial set and the structurally similar molecules) was performed using the eToxPred algorithm. According to Pu et al., a toxicity prediction threshold of 0.58 best discriminates between highly toxic and less toxic compounds. Therefore, only compounds with a toxicity prediction value below 0.58 were retained."

<p align="center"> 
  <img src="https://github.com/pawlakG/pharmD/blob/f141e3fb89491a4eb6d30d92290f41df89e236b8/output/img/pharmD_Outline.png" width=40% height=40%>
</p>
<p align="center">
  <em>Figure 1: PharmD practical project outline.</em>
</p>

## Active compound on MET and filtering

Following the search for compounds active on the MET receptor, 4,206 IC50 assays were retrieved for 3,204 molecules, with pIC50 values ranging from 3.585 to 9.88 and an average value of 7.25 (Figure 2).

<p align="center"> 
  <img src="https://github.com/pawlakG/pharmD/blob/8e526862e84ebb55294353f952da5fcc67169a07/output/img/activMolMET.png" width=40% height=40%>
</p>
<p align="center">
  <em>Figure 2: IC50 histogram of MET active compounds.</em>
</p>

After filtering based on Lipinski's rules, as well as removing over-interacting substructures and undesirable structural motifs, 1,308 molecules were selected (Figure 3).

<p align="center"> 
  <img src="https://github.com/pawlakG/pharmD/blob/8e526862e84ebb55294353f952da5fcc67169a07/output/06_similarCompoundMolecularFiltering/simCompoundFiltered.png" width=40% height=40%>
</p>
<p align="center">
  <em>Figure 3: Radar plot representig globel Lipinski indicators for selected compounds.</em>
</p>

## Similar active compounds

From the 1,308 selected molecules, 73,505 structurally similar compounds (with at least 75% similarity) were extracted from the PubChem database. Of these, 66,816 complied with Lipinski's rules, and after identifying 13,687 compounds containing over-interacting or undesirable motifs, the number of filtered molecules was reduced to 53,129.

A deep learning model was applied to predict the pIC50 of all the obtained molecules. This model consists of a deep neural network with two hidden layers of 64 and 32 neurons. It was trained on the initial set of MET-active compounds, divided into a training set of 915 molecules and a test set of 393 molecules. The model predicted pIC50 values with a mean absolute error of 0.68 and a mean squared error of 0.82. This model is applied to predict the pIC50 values for the second set of selected molecules (Figure 4).

<p align="center"> 
  <img src="https://github.com/pawlakG/pharmD/blob/60bda58367db9f016b267f0509dc13b0a5d74a2f/output/img/ic50PredSimCompounds.png" width=40% height=40%>
</p>
<p align="center">
  <em>Figure 4: Histogram of predicted pIC50 of similar compounds.</em>
</p>

To select only the most active compounds on the MET receptor, we retained only those with a pIC50 value below 9. After this filtering process, 89 molecules were selected. Figure 5 illustrates the 8 most active compounds along with their respective pIC50 values.

<p align="center"> 
  <img src="https://github.com/pawlakG/pharmD/blob/60bda58367db9f016b267f0509dc13b0a5d74a2f/output/img/top8ActivesMol.png" width=40% height=40%>
</p>
<p align="center">
  <em>Figure 5: Top 8 of active compounds against MET receptor.</em>
</p>

## Final compounds set

The final set of compounds comprises the initial group obtained from experimental IC50 assays on the MET receptor (1,308 molecules) and the second group of compounds retrieved based on a structural similarity of at least 75% with the initial set (89 molecules) that have a predicted pIC50 greater than 9. The final dataset contains a total of 1,397 molecules. The eToxPred algorithm was employed to predict the toxic potential of the compounds based on their SMILES encoding. Out of these, 1,344 molecules exhibited a toxicity value below 0.58. Figure 6 displays the 10 compounds predicted to be the least toxic by the eToxPred algorithm.

<p align="center"> 
  <img src="https://github.com/pawlakG/pharmD/blob/60bda58367db9f016b267f0509dc13b0a5d74a2f/output/img/top10LessToxic.png" width=40% height=40%>
</p>
<p align="center">
  <em>Figure 5: Top 10 of active and less toxic compounds against MET receptor.</em>
</p>

## Discussion

Utilizing publicly accessible or easily accessible databases, such as DrugBank, ChEMBL, PubChem, PDB or even Pubmed, for academic research purposes presents a significant opportunity to access high-value research data. Numerous databases exist for various types of biomedical data, including genomic, metabolic pathway, phenotypic, molecular, and screening data. It is possible to construct, as we have done, an analytical workflow that allows for the selection of a limited number of candidate molecules to be tested in the laboratory, within a constrained timeframe and budget.

Our application example represents only the first part of an analytical workflow. Ultimately, we select molecules based solely on their predicted or actual median inhibitory concentration on the MET receptor, as well as their potential toxicity. To enhance this analysis, molecular docking studies between the candidate molecules and the MET receptor, including its inhibition sites, should be performed. Additionally, investigating known adverse effects associated with the selected compounds and retrieving omics data from tumor cell lines harboring the METex14 mutation could further advance the analysis toward a cellular model.


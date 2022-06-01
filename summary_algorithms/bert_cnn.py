
from transformers import pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
article = '''reported in two case studies Sandler et al 2000 Rodakis 
2015 However high use of different antibiotics in children 
who subsequently developed autism was shown in a num
ber of observational studies Fallon 2005 Niehus and Lord 
2006 Bittker and Bell 2018 Hypothetically these observed 
effects could be attributable to microbiota alterations trig
gering a disturbed immune response and the release of 
cytokines thus affecting the function of the central nerv
ous system  Recently a number of 
observational studies have assessed a possible association of 
earlylife antibiotic exposure and subsequent development 
of ASD Here we aimed to systematically document avail
able evidence on the association between early life antibiotic 
exposure and the prevalence of ASD later in in childhood
Methods
InclusionExclusion Criteria for the Review
Cohort studies case–control studies and crosssectional 
studies  were  eligible  for  inclusion  in  this  review  The 
included  studies  needed  to  investigate  an  association 
between pre andor postnatal antibiotic exposure and sub
sequent diagnosis of ASD We included studies in which 
women during any trimester of pregnancy or infants and
or children underwent antibiotic treatment We focused on 
earlylife antibiotic exposure that preceded a diagnosis of 
ASD which is usually established after the second year of 
life  Studies on antibiotic exposure in 
breastfeeding mothers and subsequent risk of ASD in their 
children were not included Since the hypothesized link 
between ASD and antibiotic use is based on the aforemen
tioned microbiomegutbrain axis mechanism only stud
ies which reported data on systemic andor oral antibiotic 
therapy were taken into an account Any antibiotic types 
and doses as well as any treatment durations and indica
tions were admissible as long as the therapy fulfilled the 
aforementioned criteria Studies that reported data on anti
biotic use collectively  
or that did not report numerical data were excluded Studies 
in which the data on antibiotic use was collected only for the 
purpose of baseline characteristic of participants with no 
analysis of the association between antibiotic use and ASD 
were also excluded
Our outcome of interest was the diagnosis of ASD during 
childhood Studies in which the diagnosis was made accord
ing to established criteria such as those described in the 
Diagnostic and Statistical Manual of Mental DisordersV 
 as well as stud
ies in which ASD was reported by parents caregivers or 
doctors without any described specific criteria were avail
able for inclusion Studies that reported data on ASD only 
collectively with other neurodevelopmental disorders eg 
together with attentiondeficit hyperactivity disorder were 
excluded Only studies that compared children with ASD up 
to 18 years of age to generally healthy children without this 
diagnosis were included
Search Methods
A systematic literature search was performed on 28th of 
August 2018 with no language or publication date restric
tions The databases searched were PubMed Embase and 
PsycINFO After drafting the first version of the manuscript 
we ran a search update on the 11th of December 2018 The 
full search strategies for PubMed and Embase are presented 
in Online Resource 1 Additionally reference lists of identi
fied observational studies and relevant review articles were 
manually screened
Study Selection
Three authorsreviewers  independently 
screened the title of each study identified with the search 
strategy as well as the abstracts of potentially relevant arti
cles Subsequently the full text for each study potentially 
relevant after abstract screening as well as that for studies of 
unclear relevance was retrieved Each author independently 
assessed the eligibility of the articles and in cases of a disa
greement resolved differences by discussion
Data Extraction and Risk of Bias Assessment
Data were extracted with the use of a standard data extrac
tion form The extracted data included study year country 
design population definition of exposure definitions of 
cases and controls  definition of 
outcome  results confounding factors 
and data collection methods We extracted and reported all 
the data using the same terminology as the authors of the 
original articles
Risk of bias was assessed using the Newcastle–Ottawa 
Scale   in which the reviewers 
assign stars in all predefined bias domains In the com
parability domain the reviewers have to assign 0 1 or 2 
stars on the basis of the number and types of confounding 
factors controlled for Multiple important confounding fac
tors may play a role in studies on the antibioticASD asso
ciation including those related to different demographics 
pregnancyrelated complications mothers’ obstetrical histo
ries child characteristics at birth infections environmental 
exposures and healthcare use  The NOS 
requires the reviewers to assign stars depending on two cho
sen most important factors After the literature search and 
discussion we found no rationale to decide whether any of 
the abovementioned factors was more important than the 
others Therefore we decided to assign zero stars to stud
ies in which no confounding factors were controlled for or 
the adjustment was unclear and two stars to studies which 
controlled for any confounding factors Additionally for 
informative purposes we present confounders identified in 
each study in a separate table We decided to present risk 
of bias only descriptively and no collective score for the 
included studies was counted
Data Analysis
A metaanalysis of the findings was performed if at least two 
studies of the same type  reported the 
adjusted odds ratios  or adjusted hazard ratios  
of ASD being diagnosed in participants exposed to antibi
otics during the same life period  We 
performed the metaanalyses using the Review Manager 53 
software by the Cochrane Collaboration Generic inverse 
variance with the random effects model was used Addition
ally the fixed effects model was applied to see how it would 
influence the results To enable a graphic presentation of the 
findings in studies which didn’t report OR or HR we calcu
lated crude ORsHRs and 95 confidence intervals  
of ASD being diagnosed after antibiotic exposure provided 
the data were sufficient
Journal of Autism and Developmental Disorders  493866–3876
Results
Overall Characteristics
In total we identified 6820 records by the database search 
and 891 records by reference screening After exclusion 
of duplicates and title and abstract screening the full 
texts of 63 articles were assessed for eligibility Thirty
seven observational studies on risk factors for autism were 
excluded because they did not report antibiotic exposure 
Reasons for exclusion of the remaining 15 studies are 
listed in Online Resource 2 After fulltext assessment 
11 articles ultimately met the inclusion criteria for this 
review The flow diagram of the selection process is pre
sented in Online Resources 3 and 4 present characteristics and 
main results of the included studies Four of those studies 
were cohort studies and seven of them were case–con
trol studies Among the included cohort studies three 
Danish studies Atladottir et al 2012 Wimberley et al 
2018 Axelsson et al 2019 were performed in overlap
ping populations Five studies examined prenatal antibiotic 
exposure five assessed early childhood antibiotic exposure 
and 1 study examined both types of exposure Wimberley 
et al 2018 In the majority of included studies use of any 
antibiotic for any indication and duration and at any dose 
within the defined time period was analyzed Addition
ally all of the cohort studies and two of the case–control 
'''


summary = summarizer(article, max_length=130, min_length=30)
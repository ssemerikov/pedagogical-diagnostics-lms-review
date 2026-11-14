# Forecasting-model specification

This document restates the forecasting model of the article *Pedagogical diagnostics as a basis for educational
recommendation systems: LMS-integrated forecasting of learning technology effectiveness*. It follows three
subsections of the article: "Mathematical formulation of forecasting", "What the forecast can and cannot claim"
and "Validation protocol". It uses their symbols and introduces no symbol or claim of its own. Where this file and
the article differ, the article is authoritative.

**Status.** This is a design specification. None of it has been run on course data, and no forecast accuracy has
been established. The authors' prototype is not part of this repository and its source code is not publicly
available. This repository contains no implementation of the model.

## Provenance tags

Every item is tagged with where it comes from.

| Tag | Meaning |
|---|---|
| **[monograph]** | Stated in the published monograph: O. H. Kolgatin, *Pedagogical Diagnostics as a Basis for Educational Recommendation Systems*, Simon Kuznets Kharkiv National University of Economics, Kharkiv, 2026 (in Ukrainian). |
| **[authors' current design]** | The authors' current design, which goes beyond the published monograph. |
| **[this revision]** | Proposed in the revised version of the article, and not in the monograph. This includes properties of the formulation first stated in the revision. |
| **[submitted article]** | Stated in the article as first submitted, and not attributed there to the monograph. |

## 1. Architecture: the triad

- **[monograph]** The system rests on three information models, each realised as a set of relational database
  structures.
  - The Learning Goals Model ($M_{CN}$) holds the educational objectives, the teaching methods available for
    reaching them, and the structure of the learning-material content.
  - The Psychological-Pedagogical Student Model (PPSM) holds, for each student, a dynamic record of learning
    achievement together with indicators of psychological and physiological properties.
  - The Learning Technology Implementation Model ($M_{RTN}$) holds the learning-technology variants, the
    requirements attached to each, and the data from which their effectiveness is forecast.
- **[submitted article]** The mastery coefficients $K_1$, $K_2$, $K_3$ (Section 2) are the common currency of
  the architecture. $M_{CN}$ states the levels an element targets, the PPSM records the levels a student has
  reached, and $M_{RTN}$ carries the forecast of the levels a variant is likely to produce.
- **[this revision]** The PPSM serves two purposes, which the model keeps apart.
  - Its *descriptive layer* is the profile that a student and a teacher discuss. **[monograph]** It holds the
    indicators of the published model, in four groups: motivation and goals, mastery of the content,
    self-management and activity, and reflection and prognosis.
  - Its *predictive layer* is the forecaster's input vector $\mathbf{s}$ (Section 3), and nothing else.
- **[this revision]** The Ehrman and Leaver (E&L) dichotomies belong to the descriptive layer. They are not
  forecaster inputs, and nothing in a forecast depends on them. The submitted article already stated that they
  are not among the inputs. The LMS indicators proposed for them are given in
  [Supplementary Material S4](../data/supplement/S4_EL_operationalisation.md) and are uncalibrated.
- **[monograph]** The requirements attached to each variant form a separate category of input. They are applied
  before forecasting to determine which variants the student is eligible for, and a student who does not meet an
  achievement prerequisite is advised to master the preceding elements first.
  - **[this revision]** These eligibility conditions are evaluated on the achievement records for named
    prerequisite elements and on indicators of the descriptive layer, for example a threshold on systematicity.
    They are not part of the input vector $\mathbf{s}$. They are the only route by which descriptive-layer
    indicators reach the system's decisions.

## 2. Outcome: mastery coefficients and the objective

- **[monograph]** The forecasting problem: for a learning-material element $\ell$ and a student whose PPSM record
  is denoted $\mathbf{s}$, choose one of the available learning-technology variants $t \in T_\ell$ so as to
  maximise the student's predicted mastery of $\ell$.
- **[monograph]** The grade for the element is not the outcome. The composition of a grade changes over time as
  assessment criteria and the weighting of required work are revised, so a model trained on grades from earlier
  cohorts learns partly about the rubric rather than about the student.
- **[monograph]** The outcome is expressed through three mastery coefficients, each the proportion of the
  element's requirements met at one level:
  - $K_1$, average level: knowledge of the obligatory facts, and performance of tasks at the reproductive level;
  - $K_2$, sufficient level: use of that knowledge to solve problems whose solution method has already been
    covered;
  - $K_3$, high level: application of knowledge to novel problems in a new situation (transfer, evaluation,
    synthesis and analysis).
- **[authors' current design]** Each coefficient is a ratio. This is the authors' operational definition, given
  so that the coefficients can be reproduced; the monograph defines the three levels but not how each coefficient
  is computed.
  - $K_1$: the obligatory facts and reproductive operations the student has mastered, relative to the number
    that the curriculum requires for the element;
  - $K_2$: the operations the student performs correctly, relative to the number required to solve the standard
    problems that the curriculum prescribes;
  - $K_3$: the creative, analytical and evaluative operations the student performs successfully, relative to the
    number of non-standard problem-solving operations that the assessment tasks present.
  - **[monograph]** The monograph defines the completeness of a student's knowledge in the same way, as the
    ratio of the facts the student knows to the number the programme requires.
- **[submitted article]** Each coefficient lies in $[0,1]$. It is computed from the gradebook records for the
  assessment items attached to the element, which are classified by level when the element is authored. The
  three coefficients correspond to the reproductive, applied and transfer strata of a Bloom-type hierarchy.
- **[this revision]** A comparable progression runs through the skills descriptors of the levels of Ukraine's
  National Qualifications Framework (Cabinet of Ministers of Ukraine, 2011). It goes from performing standard
  tasks in typical situations to finding creative solutions and, at the higher levels, to innovative activity
  that develops new knowledge.
- **[submitted article]** Time spent on the element would be a valuable fourth component and is deliberately
  absent. Much independent work happens outside the LMS, in tools that record nothing, and asking students to
  report their own time would both burden them and yield poor recall.
- **[monograph]** The objective function and its constraint:

$$F = K_1 W_1 + K_2 W_2 + K_3 W_3, \qquad W_1 + W_2 + W_3 = 1.$$

  The course author or teacher sets the weights $W_1$, $W_2$, $W_3$ to reflect the cognitive level that the
  element targets. An element that only needs to be recognised carries a high $W_1$; an element that must be
  applied to novel problems carries a high $W_3$.

## 3. The input vector s

- **[monograph]** The student description $\mathbf{s}$ is deliberately small. The number of training cases
  available for any one element is small, and the input dimension has to be kept in proportion to it. It
  comprises:
  - the mastery coefficients $K_1$, $K_2$, $K_3$ carried forward from the elements preceding $\ell$, each the
    arithmetic mean of the corresponding coefficient over those elements; and
  - five parameters characterising the student's style of learning activity, listed below.
- **[this revision]** The notation $P_1, \dots, P_5$ for the five parameters, in the order of the monograph's
  list, is the article's. The names below are copied from the article's table of parameters (`tab:params`).

| Symbol | Parameter |
|---|---|
| $P_1$ | significance of the result of the work |
| $P_2$ | interest in the learning process and cognitive interest |
| $P_3$ | stability of working tempo |
| $P_4$ | capacity to mobilise energy, persistence and will |
| $P_5$ | reflection |

- **[this revision]** Nothing else enters $\mathbf{s}$. In particular, the E&L dichotomies, the other
  descriptive-layer indicators and the systematicity coefficient are not inputs. The systematicity coefficient
  informs the present valuation of $P_3$ (Section 3.2).
- **[this revision]** None of these features has yet been validated as a predictor. Whether they predict
  anything is what the validation protocol tests (Section 7).

### 3.1 What the cited studies offer

- **[monograph]** The monograph's review of the included studies collects, for each parameter, the LMS indicators
  it relates to those studies. The second column of the table in Section 3.3 summarises them as the monograph
  reads them.
- **[this revision]** The re-extraction made during the review update reads the studies less generously: four of them
  analyse no per-student platform record at all, and a fifth uses platform records only as classroom averages.
  The column therefore states what the monograph drew from the literature, not what each study measured. The
  three that do relate a platform-recorded indicator to an outcome each report a coefficient, but none was
  designed to measure the parameter as it is defined here.
- **[monograph]** The monograph records two gaps in them. The studies that bear on reflection either give no
  concrete mechanism for assessing it or rely on self-report. None gives a mechanism for determining cognitive
  interest as such: interest in the process of learning activity has to be distinguished from cognitive interest
  proper.
  - **[authors' current design]** That no published indicator separates the two is the authors' current reading
    of the literature.

### 3.2 How the design obtains a value

- **[monograph]** When a student requests a forecast, the parameters are computed automatically from the LMS data
  and offered to the student and the teacher for confirmation. They are interpreted in the light of the student's
  self-analysis and the teacher's pedagogical observations, compared with the values previously held, and updated
  only with the agreement of both. The monograph also proposes self-analysis with the teacher's help, based on the
  student's own digital footprint, as the way such characteristics are established in the first place, in
  preference to a psychological questionnaire.
- **[authors' current design]** A parameter for which no LMS indicator is available or reliable takes its value
  from that self-analysis alone. In the proposal of Section 3.3 this applies to two of the five ($P_1$ and $P_5$),
  and to any parameter whose LMS value is undefined for want of records.
- **[authors' current design]** Until the computation from LMS records is built, every parameter is valued by the
  student's self-analysis and the teacher's pedagogical observation. In the prototype the value is entered on the
  scale $[0,1]$ of the mastery coefficients, and it enters a forecast only after the teacher has approved it.
  - **[this revision]** How a self-analysed value is best placed on that scale is a question for the calibration
    study.
- **[authors' current design]** The one formula the authors use at present to inform such a valuation is the
  share of assignments completed and submitted on time out of all assignments.
  - **[monograph]** It is the systematicity coefficient of Kolgatin, Holubnychyi and Kolgatina (2020), on which
    the monograph bases the diagnosis of the stability of working tempo, so it bears on $P_3$.

### 3.3 Proposed operational definitions

- **[this revision]** The monograph states that the parameters are computed from LMS data but not how. The
  definitions in the last column below are therefore the authors' proposal, made in the revision so that the
  specification can be reproduced. They are not in the monograph and have not been calibrated; their calibration
  is part of the validation protocol (Section 7).
- **[this revision]** The definitions use only records that Moodle keeps for any course: the opening and due dates
  of assessed activities, the times and grades of submission attempts, and the log of resource views. The
  observation window is the one used for the carried-forward coefficients, the elements preceding $\ell$.
- **[this revision]** For an assessed activity $a$ in that window, with opening time $o_a$ and due time $d_a$, the
  position of student $i$'s final submission time $u_{ia}$ within the time available is

$$r_{ia} = \min\Bigl(1,\ \max\Bigl(0,\ \frac{u_{ia} - o_a}{d_a - o_a}\Bigr)\Bigr),$$

  with a late submission set to 1. Activities the student did not submit are left out. Each $r_{ia}$ lies in
  $[0,1]$, so its standard deviation over activities is at most $1/2$, and the definition of $P_3$ below also
  lies in $[0,1]$.

In the table, "confirmed" means offered to the student and the teacher for confirmation. **[authors' current
design]** Until the LMS computation is built, all five parameters are valued by self-analysis and the teacher's
observation, and any parameter whose definition is undefined for a student falls back to self-analysis. All values
lie in $[0,1]$.

| Parameter | Indicators in the cited studies **[monograph]** | Value from | Proposed operational definition **[this revision]** |
|---|---|---|---|
| $P_1$ significance of the result of the work | Self-efficacy and perceived usefulness of online learning, by questionnaire (Udin et al., 2022); behavioural-engagement patterns related to final grades (Hsueh et al., 2022) | Self-analysis with the teacher | None from LMS records: no indicator in the cited studies separates the significance of the result from that of the process, a distinction the monograph asks for |
| $P_2$ interest in the learning process and cognitive interest | Frequency and duration of access to particular learning objects (Herrera-Granda et al., 2024); video viewing, forum participation and regular access to supplementary material (Hsueh et al., 2022); time spent and autonomy in a virtual-reality environment (Farameita et al., 2025) | LMS, confirmed | Share of the optional (ungraded) resources of the preceding elements that the student opened at least once; undefined if there are none. Does not separate the two kinds of interest |
| $P_3$ stability of working tempo | Share of reports submitted by the deadline (the systematicity coefficient), and the interval from first access to the materials to final upload, which collapses before the deadline under rush work (Kolgatin et al., 2020); regularity of video viewing and self-tests (Hsueh et al., 2022) | LMS, confirmed; at present informed by the share of assignments submitted on time | $1 - 2\,\mathrm{sd}_a(r_{ia})$, with $r_{ia}$ as above, over the assessed activities the student submitted in the window; undefined for fewer than two |
| $P_4$ capacity to mobilise energy, persistence and will | Self-directed learning in a gamified LMS (Ferdiansyah et al., 2025); academic self-efficacy (Udin et al., 2022); timeliness of submission (Kolgatin et al., 2020), whose reading as volitional self-regulation is the monograph's, not the study's | LMS, confirmed | Share of the student's unsuccessful graded attempts (below the activity's pass mark) that are followed by a further attempt before the activity closes; undefined if there were none, or if the activities allow one attempt only |
| $P_5$ reflection | No mechanism for measuring it is given (Kolgatin et al., 2020; Ferdiansyah et al., 2025); self-reports in questionnaires and feedback forms (Savchuk et al., 2019; Bykonia et al., 2019); perceived autonomy and satisfaction (Farameita et al., 2025) | Self-analysis with the teacher | None from LMS records |

- **[this revision]** $P_3$ rewards a constant position of submission within the available time, not an early
  one. A student who always submits at the last moment scores high on it. This departs from the cited reading of
  last-minute work as a loss of stable tempo, and it is one of the points the calibration study has to settle.
- **[this revision]** The systematicity coefficient (the share of required reports submitted by their deadlines)
  informs the present valuation of $P_3$ but is not itself an input. It stays in the descriptive layer of the
  PPSM, where $M_{RTN}$ uses it as an eligibility condition. The correlation reported for it is with assessment
  outcomes in one sample, and it establishes neither the coefficient nor the proposed definition of $P_3$ as a
  predictor.
- **[this revision]** The two measure different things: the coefficient rewards punctuality, and the proposed
  $P_3$ rewards constancy of timing. Which of them better captures the stability of working tempo is for the
  calibration study to settle.
- **[this revision]** $P_3$ and $P_4$ are both computed from submission records, so their values will be
  correlated. Whether they measure different things is for the calibration study to establish; nothing in the
  definitions guarantees it.

## 4. Estimate, recommendation and loss

- **[monograph]** For each available variant $t \in T_\ell$, the forecasting model produces an estimate
  $\hat{F}(\mathbf{s}, \ell, t) \in [0,1]$ of the value of $F$ that the student is likely to achieve. There is one
  forecast per variant, and the variant the system puts forward is

$$t^*(\mathbf{s}, \ell) = \arg\max_{t \in T_\ell} \hat{F}(\mathbf{s}, \ell, t).$$

  - **[authors' current design]** The forecasting model is not fixed in advance; a neural network is one
    possibility (Section 5).
- **[monograph]** The model is trained by minimising the deviation between predicted and observed objective
  values, over all students who have previously completed $\ell$ under one of the available variants.
  **[submitted article]** It is written as a sum of squares:

$$L = \sum_{i \in D_\ell} \bigl( \hat{F}(\mathbf{s}_i, \ell, t_i) - F_i \bigr)^2,$$

  where $D_\ell$ is the set of historical training cases for $\ell$, $t_i$ is the variant student $i$ took, and
  $F_i$ is the observed value of $F$.
- **[this revision]** For each training case, $L$ contains only the output for the variant that student took,
  $t_i$; the outputs for the other variants do not enter it. The loss is *masked* in this sense: the output for
  variant $t$ receives error signal only from students who took $t$. Parameters shared between the outputs, such
  as the hidden layers of a network with one output per variant, would be fitted on all the cases in $D_\ell$. A
  separate model for each variant shares none. Nothing is imputed for the variants a student did not take.
- **[monograph]** This is the monograph's formulation, which builds the estimate for a variant by comparing the
  intended learning outcomes of the element with the actual achievements of the students who chose that variant.
- **[authors' current design]** The prototype, whose source code is not publicly available, realises $L$ with no
  parameters shared across variants.
  - For each variant of an element it fits a separate regression model, only to the cases of the students who
    took that variant.
  - The inputs are the five parameters and the coefficients $K_1$, $K_2$, $K_3$ carried forward as their means
    over the elements named as that variant's prerequisites. Unlike the specification above, the carried-forward
    input can therefore differ between the variants of one element. The target is the value of $F$ on the
    element.
  - The model is chosen with the model-comparison routine of PyCaret 3 (PyCaret Core Team, 2023), which fits its
    default set of regressors and ranks them by mean squared error under 10-fold cross-validation. The best of
    them gives the forecast and is stored with the variant. In PyCaret 3 that default set leaves out the
    multilayer-perceptron regressor, so as built the comparison fits no neural network unless one is added to it
    explicitly.
  - No minimum number of cases is enforced. A variant with no cases receives no forecast, so $n_{\min}$ (below)
    remains a parameter of the protocol.
  - The authors' intention is that a model be fixed as a component of $M_{RTN}$ for an element only once enough
    data have accumulated.
  - The cross-validated selection is made within the training data, so it does not replace the held-out
    comparison with the baselines of Section 5. None of it has been run on course data.
- **[this revision]** Two consequences of the masked loss follow.
  1. *Thin data.* A variant that few students choose has few cases behind its output, and its estimate is
     correspondingly unreliable. A rule the monograph does not contain is therefore added: the forecast for a
     variant with fewer than $n_{\min}$ training cases for the element is withheld and shown as resting on
     insufficient data, not as a low score. $n_{\min}$ is set in the validation protocol, not in advance. The
     recommendation $t^*$ is then taken over the variants that have a forecast. If none has, no recommendation is
     made and the student chooses without one.
  2. *Selection.* The students behind each output chose that variant, so its estimate describes them and not the
     class as a whole (Section 6).

## 5. Training procedure and choice of estimator

- **[monograph]** The unit of training is one case per student and completed element. For a student who has
  completed $\ell$ under one of its variants, the case holds the student's PPSM input vector, the variant taken
  and the observed value of $F$.
  - **[this revision]** The input vector is the one that stood when the student began $\ell$, since the record
    changes as the course proceeds.
- **[monograph]** A separate model is fitted for each learning-material element, over the variants attached to it,
  from the PPSM records of the students who have already studied that element. The records are held without any
  link to the students' personal data, so their use needs no individual permission.
- **[this revision]** The candidate estimators are tuned by cross-validation within the training cohorts only. For
  evaluation the cases are split by cohort rather than at random: a model fitted on earlier cohorts is frozen and
  scored on a later cohort that played no part in fitting or tuning it. The primary measure is the mean absolute
  error between $\hat{F}(\mathbf{s}_i, \ell, t_i)$ and the observed $F_i$ for the variant each student took.
- **[monograph]** In routine operation the model for an element is refined whenever a forecast for that element is
  requested, using all the records accumulated so far.
  - **[this revision]** For the validation period, a refit once per cohort replaces this. Every forecast issued to
    a cohort then comes from the same frozen model, and each cohort serves as the held-out test set for the model
    fitted on its predecessors.
- **[monograph]** The monograph specifies a neural network as the estimator and defers a comparison of network
  structures until enough experimental data have accumulated.
- **[this revision]** The network is treated as one candidate class rather than as the method. The number of cases
  per element is small, and with few cases a flexible estimator can fit its training data better than a simple
  one while predicting new students worse.
  - **[authors' current design]** In the authors' current design, too, the regression method is chosen by
    comparison rather than fixed in advance, and neural-network models can be applied only after a considerable
    volume of data has accumulated.
- **[this revision]** The design fixes a ladder of baselines. Each is fitted to the same cases and inputs and
  evaluated on the same held-out cohort.
  1. The best-average variant, which recommends to every eligible student the variant with the highest mean
     observed $F$ and uses no information about the student. Any personalisation has to justify itself against
     it.
  2. Ridge regression on the input vector, fitted separately for each variant.
  3. A regression tree of small fixed depth for each variant, whose splits a teacher can read.
- **[this revision]** Adoption rule: a more flexible model, whether a neural network or the candidate the
  cross-validated comparison selects, is adopted for an element only if its out-of-sample mean absolute error is
  lower than that of the best baseline by a margin fixed before the trial. Otherwise the simplest model within
  that margin of the best is used. The margin, like $n_{\min}$, is set and registered in the validation protocol.
- **[this revision]** Every rung estimates $\hat{F}(\mathbf{s}, \ell, t)$ from the cases of students who took $t$,
  as $L$ does. The recommendation rule and the selection problem of Section 6 are therefore the same whichever
  estimator is used.
- **[this revision]** Fitting each element separately, rather than pooling cases across courses to obtain more of
  them, has independent support: in a large open and distance education dataset, about a third of the variance in
  academic performance lay between classes (Ratnaningsih et al., 2027).
- **[submitted article]** Two consequences favour this formulation. The objective is independent of the
  assessment scale used in any one course, for the reason given in Section 2. The constraint on the weights keeps
  them a property of the curriculum rather than of the student, so the model can be re-used across cohorts.

## 6. What the forecast can and cannot claim

- **[submitted article]** $D_\ell$ contains, for each past student, the variant they took and the mastery they
  achieved under it, and nothing about the variants they did not take. $L$ therefore fits a model of *observed*
  outcomes, while the recommendation asks that model to score every variant in $T_\ell$, including those the
  student was never exposed to. Students who chose a given variant may differ systematically from those who did
  not, in ways the PPSM does not capture. The model has no way to separate the effect of the variant from the
  reasons it was chosen.
- **[this revision]** The masked form of $L$ (Section 4) is where this enters the estimates: the output for each
  variant is corrected only by the outcomes of the students who chose it.
- **[submitted article]** What the forecast supports is a statement of the form: among past students whose records
  resemble this one, those who took variant $t$ reached this level of mastery. That is not the counterfactual
  claim that this student would do better under $t$ than under $t'$.
- **[submitted article]** The system's own recommendations shape which variants get taken. Later training data
  therefore reflect the model's earlier behaviour, and without intervention the estimates for rarely recommended
  variants degrade for want of observations.
- **[submitted article]** The standard remedy, assigning students to variants at random, is not straightforwardly
  available here, and the reason is pedagogical rather than practical. The design gives the student the final say
  over whether to accept the system's advice; a student who must take an assigned variant is no longer exercising
  the choice the system exists to inform.
- **[monograph]** The student's final say follows from the student-centred and axiological commitments of the
  approach. The monograph accordingly rejects fixed control and experimental groups. It proposes instead that the
  system assign students dynamically to comparison groups while analysing the quality of particular branches of
  the forecast.
- **[submitted article]** That procedure yields a continuous internal audit of the forecasts and respects student
  choice, but it does not solve the identification problem: students still select their variant, so the
  comparison remains observational. The two purposes are therefore separated.
  - Dynamic assignment is the mechanism for routine quality monitoring in normal operation.
  - For the validation study, a bounded departure is warranted. Students who consent may be allocated at random
    among the variants they are eligible for, for a subset of learning-material elements and a limited period.
    Nobody is enrolled without consent, and consent may be withdrawn.
  - **This departs from the monograph's evaluation design, and the article flags the departure.**
  - Without such a period, no amount of accumulated operational data will establish that the system's
    recommendations cause better outcomes rather than merely predicting them.
- **[submitted article]** Until that work has been done, the system's output should be read as evidence for a
  decision the student and teacher make, not as a prediction of what each variant would produce.

## 7. Validation-trial protocol

None of this has been carried out, and nothing below is a result.

- **[this revision]** The quantities the protocol leaves open are fixed and registered before any data are
  collected: the minimum number of training cases per variant $n_{\min}$, the margin by which a more flexible
  model has to beat the baselines, and the radius of the weight neighbourhood (Section 8).
- **[this revision]** No deployment begins until institutional ethics approval has been obtained and each
  participating student has given informed consent, which may be withdrawn at any time without consequence.
- **[submitted article]** The trial runs across several courses. Students who consent are allocated at random
  among the eligible variants for a subset of learning-material elements, which is what makes the resulting data
  able to support the counterfactual claim the forecaster is asked for.
  - **[this revision]** The allocation is bounded in time and in the elements it covers. Outside those bounds the
    student chooses, as in normal operation.
  - **[this revision]** For every element, the variant each student takes, whether allocated or chosen, is logged
    together with the forecast that was shown.
- **[authors' current design]** Trial data would accumulate in a cycle.
  - The variant a student takes for an element would be recorded with the element and with the forecast that was shown.
  - At the student's next session, the mastery coefficients achieved on that element would be retrieved, the case
    added to the training data of the variant taken, and the forecast compared with the outcome.
  - In routine operation the variant's model would be refitted at that point. **[this revision]** During the trial the
    refit follows the once-per-cohort rule of Section 5, so the comparisons accumulate against a frozen model.
  - Two links in the cycle remain to be built: the prototype stores the choice without the forecast, and it
    simulates the Moodle data from which achievements would be retrieved.
  - **[this revision]** Outside the randomised subset the cycle yields observational data. Its comparisons of
    forecast with outcome are then the internal audit of Section 6, not evidence that following a recommendation
    improves outcomes.
- **[this revision]** The outcomes are the mastery coefficients $K_1$, $K_2$, $K_3$ for each element and the
  objective $F$ computed from them under the weights the authoring team set. Because the three coefficients are
  stored, $F$ can be recomputed under any other weights.
- **[this revision]** The trial measures the forecast against observed mastery using mean absolute error against
  the baseline ladder of Section 5. **[submitted article]** It compares the recommended variant against student
  and teacher choice on learning outcomes.
- **[this revision]** The primary analysis is out of sample. Each cohort is forecast by a model frozen after
  fitting on its predecessors, and a more flexible model is retained for an element only if it beats the best
  baseline by the registered margin.
- **[this revision]** Within the randomised subset, students whose allocated variant coincided with the
  recommended one can be compared with those whose did not. This estimates what following the recommendation is
  worth without the selection described in Section 6.
- **[this revision]** The same subset tests a hypothesis set out in the article's literature review: that students
  whose records show irregular, deadline-driven submission gain more from externally scaffolded variants than from
  self-paced ones. It is tested as an interaction between the systematicity indicator and the type of variant. The
  forecaster does not read the systematicity indicator itself, which at present only informs the valuation of
  $P_3$, so it can pick up this mechanism only through $P_3$, $P_4$ and the carried-forward coefficients.
- **[this revision]** The weight-sensitivity analysis of Section 8 is run for every element in the trial. Where a
  course has more than one teacher or author, each sets the weights for its elements independently before the
  trial begins, so that their agreement can be reported alongside the share of recommendations that change across
  the weight simplex.
- **[this revision]** The five learning-activity parameters are calibrated as measures before they are trusted as
  predictors. For each parameter the protocol estimates its stability across adjacent elements, its agreement with
  the value the student and the teacher confirm after self-analysis, and its relation to the other parameters. In
  particular it checks whether the definitions of $P_3$ and $P_4$, both computed from submission records, can be
  told apart.
  - **[monograph]** These are the kinds of reliability analysis the monograph prescribes for diagnostic data: the
    structure of the measurements, their internal consistency, comparison with results obtained by other methods,
    and comparison of repeated measurements.
  - **[authors' current design]** Defining concrete indicators for these criteria and validating them
    psychometrically is, in the authors' current view, the most pressing need in this line of work.
- **[submitted article]** A parallel sub-study administers the explicit E&L instrument alongside the LMS
  measurements on the same students. This is the only way to establish whether the behavioural indicators proposed
  in Supplementary Material S4 measure what they are assigned to measure, or whether they should be kept purely as
  behavioural descriptors. **[this revision]** Administering the instrument requires professional oversight, which
  the study design provides.
- **[this revision]** Uptake and the approval workflow are recorded as well: how often students request forecasts
  and follow them, and how teachers handle requests to change a profile.
- **[this revision]** The choice of estimator is settled within the trial rather than assumed before it.
  Interpretability remains open after it: if ridge regression or a shallow tree comes within the registered margin
  of the more flexible model, the design uses the model whose reasons a teacher can state.

## 8. The weights: provenance and sensitivity

- **[monograph]** The weights belong to $M_{RTN}$. They are set by the authoring team of the educational
  programme, or by the teacher of the discipline that contains the element, according to the programme's learning
  goals and the competence requirements that the higher-education standard defines. Some elements are
  introductory and need not be mastered at the high level at all.
- **[this revision]** The weights are non-negative, so with the constraint $W_1 + W_2 + W_3 = 1$ they lie on a
  two-dimensional simplex.
- **[this revision]** Anchoring them in programme-level requirements makes them a documented curricular decision
  rather than a private preference, but it does not remove the judgement involved. Two members of the same
  authoring team could weight the same element differently, and different weights can change which variant is
  recommended.
- **[this revision]** Sensitivity analysis (not part of the monograph's design). For each element, the
  recommendation $t^*$ is recomputed over a regular grid on the weight simplex; a step of 0.1 gives 66 weight
  vectors. Two things are reported:
  1. the share of students whose recommended variant differs from the one obtained under the weights the authors
     set, both across the whole grid and within a neighbourhood of those weights whose radius is fixed in the
     validation protocol;
  2. where two or more members of the authoring team set the weights for the same element independently, how far
     apart their settings lie, which is the most direct evidence on how reliable the weights are.
- **[this revision]** Because the estimator is fitted to observed values of $F$ computed under one set of weights,
  each grid point requires refitting it to targets recomputed from the stored coefficients $K_1$, $K_2$, $K_3$ of
  the training cases. The formulation itself is unchanged.
- **[this revision]** One case needs no computation. If the coefficients predicted for one variant are at least as
  high as those of every other variant at all three levels, that variant maximises $F$ for every admissible choice
  of weights, because the weights are non-negative. The recommendation is then invariant to $W$, and disagreement
  about the weights matters only where the predicted mastery profiles of the variants cross. Checking this
  condition requires predicting $K_1$, $K_2$ and $K_3$ for each variant rather than their weighted sum alone.
- **[this revision]** That is recorded as a design option and not adopted. An estimator with three outputs per
  variant, combined through $F$ only at the moment of recommendation, would let the weights change without
  retraining and would make the dominance check routine. The cost is three times as many quantities to estimate
  from the same small sample.

## Symbols

| Symbol | Meaning |
|---|---|
| $M_{CN}$, PPSM, $M_{RTN}$ | Learning Goals Model; Psychological-Pedagogical Student Model; Learning Technology Implementation Model |
| $\ell$ | a learning-material element |
| $T_\ell$; $t$, $t'$ | the learning-technology variants available for $\ell$; a variant |
| $\mathbf{s}$, $\mathbf{s}_i$ | the forecaster's input vector (the PPSM's predictive layer); that of student $i$ |
| $K_1$, $K_2$, $K_3$ | mastery coefficients at the average, sufficient and high levels, each in $[0,1]$ |
| $W_1$, $W_2$, $W_3$; $W$ | weights of the objective, non-negative and summing to 1; the weights collectively |
| $F$; $F_i$ | the objective $K_1 W_1 + K_2 W_2 + K_3 W_3$; its observed value for training case $i$ |
| $\hat{F}(\mathbf{s}, \ell, t)$ | the forecast of $F$ for a student with input $\mathbf{s}$ on element $\ell$ under variant $t$ |
| $t^*(\mathbf{s}, \ell)$ | the recommended variant, the arg max of $\hat{F}$ over the variants that have a forecast |
| $L$; $D_\ell$; $t_i$ | the training loss; the training cases for $\ell$; the variant student $i$ took |
| $n_{\min}$ | the minimum number of training cases for a variant's forecast to be shown (set in the validation protocol) |
| $P_1, \dots, P_5$ | the five learning-activity parameters of $\mathbf{s}$ |
| $a$; $o_a$, $d_a$; $u_{ia}$; $r_{ia}$ | an assessed activity; its opening and due times; student $i$'s final submission time; its relative position |
| $\mathrm{sd}_a$ | the standard deviation over the assessed activities in the window |

## References

- Cabinet of Ministers of Ukraine (2011). *Pro zatverdzhennia Natsionalnoi ramky kvalifikatsii* [On approval of the
  National Qualifications Framework]. Resolution No. 1341 of 23 November 2011; annex as amended by Resolution
  No. 519 of 25 June 2020. https://zakon.rada.gov.ua/laws/show/1341-2011-%D0%BF
- Bykonia, O. P., Borysenko, I. V., Zvarych, I. M., Harbuza, T. V., & Chepurna, M. (2019). Teaching Business English
  to Future Economists Using a Multimedia Textbook. *International Journal of Higher Education*, 8(4), 115–125.
  https://doi.org/10.5430/ijhe.v8n4p115
- Farameita, E., Kurniasari, F., & Tjahjana, D. (2025). Evaluation of the Integration of Learning Management Systems
  with Virtual Reality Platform. *Multidiscience: Journal of Multidisciplinary Science*, 2(2), 384–397.
  https://doi.org/10.59631/multidiscience.v2i2.404
- Ferdiansyah, H., Rafi, M. F., Utama, A. P., Aprilia, T., & Slamet, J. (2025). Assessing learning outcomes and
  self-directed learning through gamification in LMS. *Social Sciences & Humanities Open*, 12, 101696.
  https://doi.org/10.1016/j.ssaho.2025.101696
- Herrera-Granda, E. P., Loor-Bautista, J. G., & Mina-Ortega, J. I. (2024). Incidence of Metaphorical Virtual
  Classrooms and Interactive Learning Objects in the Interaction of Online Students: An Ecuadorian Case Study.
  *Applied Sciences*, 14(15), 6447. https://doi.org/10.3390/app14156447
- Hsueh, N. L., Daramsenge, B., & Lai, L. C. (2022). Exploring the Influence of Students' Modes of Behavioral
  Engagement in an Online Programming Course Using the Partial Least Squares Structural Equation Modeling.
  *Journal of Information Technology Education: Research*, 21, 403–423. https://doi.org/10.28945/5010
- Kolgatin, O. H. (2026). *Pedagogical Diagnostics as a Basis for Educational Recommendation Systems*. Kharkiv:
  Simon Kuznets Kharkiv National University of Economics (monograph, in Ukrainian).
- Kolgatin, O., Holubnychyi, D., & Kolgatina, L. (2020). Systematicity of students' independent work in the course
  of operating systems. *SHS Web of Conferences*, 75, 03009. https://doi.org/10.1051/shsconf/20207503009
- PyCaret Core Team (2023). *PyCaret 3.0 Docs*. https://pycaret.gitbook.io/docs/
- Ratnaningsih, D. J., Belawati, T., Puspitasari, K. A., & Amastini, F. (2027). Context-sensitive learning analytics
  in open and distance education: Identifying students' online learning behavior patterns in a large-scale
  Indonesian context. *The Internet and Higher Education*, 72, 101116. https://doi.org/10.1016/j.iheduc.2026.101116
- Savchuk, N. M., Sichkar, S. A., Khlystun, I. V., Shuliak, S. A., & Avramenko, V. (2019). The Interactivity of ICT
  in Language Teaching in the Context of Ukraine University Education. *International Journal of Higher
  Education*, 8(5), 84–93. https://doi.org/10.5430/ijhe.v8n5p84
- Udin, T., Maufur, S., & Riyanto, O. R. (2022). Student's Self-Efficacy and Perceptions of Online Learning on the
  Use Learning Management System. *Journal of Education Technology*, 6(1), 165–172.
  https://doi.org/10.23887/jet.v6i1.41884

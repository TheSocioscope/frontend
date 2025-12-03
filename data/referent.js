//TODO update with config file data (i.e.make it a function with config info as arg)

export const blockReasons = [
  {
    title: 'Spam',
    description:
      'Piece intended to promote a product, service or organization, or not disclosing author’s affiliation.',
    gentle_version:
      'This piece is intended to promote a product, service or organization, or it does not disclose the affiliation of its author',
  },
  {
    title: 'Offensive, rude or abusive ',
    description:
      'The language and/or content is inappropriate for a research project. ',
  },
  {
    title: 'Irrelevant to WPRN',
    description:
      'The relation to the core aim of WPRN (social sciences and humanities research on the impacts of the Covid-19 pandemic) is not clear enough.',
  },
  {
    title: 'Opinion piece',
    description:
      'Projects should be based on empirical research, or using scientific methods to bring theoretical or methodological advances. Opinion pieces, pamphlets, and commentaries should be published elsewhere.',
    gentle_version:
      'Projects should be based on empirical research, or using scientific methods to bring theoretical or methodological advances. Opinion pieces, pamphlets, and commentaries, however interesting and smart, should be published elsewhere.',
  },
  {
    title: 'Multiple posting of similar pieces',
    description:
      'Please post one single abstract for a set of similar or connected papers rather than several distinct abstracts. Possibly with a link  to a URL containing the set.',
    gentle_version:
      'Please upload one single contribution for a set of similar or connected papers rather than several distinct abstracts. You can include a link to a URL containing the set.',
  },
  {
    title: 'Serious methodological limitations or flaws',
    description:
      'The submission does not currently reach the threshold of work that would be considered for publication in a peer-reviewed journal.',
    gentle_version:
      'In its current form, your project has apparent limitations or methodological flaws that need to be dealt with before it can appear in the base.',
  },
  {
    title: 'Other',
    description: 'Indicate the reason why you block this project',
    gentle_version: '',
  },
]

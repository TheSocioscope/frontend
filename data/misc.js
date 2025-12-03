export const links = function () {
  return [
    {
      action: () => this.$emit('showCredits'),
      text: 'misc.seeFullCredits',
    },
    {
      to: '/privacy_policy',
      text: 'misc.privacyPolicy',
    },
    {
      to: '/guidelines',
      text: 'referents.guidelines',
      excludeRoutes: [
        'login',
        'forgot_password',
        'recover_password',
        'enroll',
        'enroll-key',
        'privacy_policy',
      ],
      for: ['referent'],
    },
    {
      to: '/press_room',
      text: 'pages.pressroom.title',
      for: ['root'],
    },
    {
      to: '/resources',
      text: 'pages.resources.title',
      for: ['root'],
    },
    {
      action: () => {
        this.$store.commit('contact/open', { id: 0 })
      },
      text: 'contact.title',
    },
  ]
}
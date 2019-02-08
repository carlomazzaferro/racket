export const config = {
  siteName: 'Racket',
  copyright: 'Racket Dashboard  © 2018 carlomazzaferro',
  logoPath: '/logo.svg',
  apiPrefix: '/api/v1',
  fixedHeader: true, // sticky primary layout header

  /* Layout configuration, specify which layout to use for route. */
  layouts: [
    {
      name: 'primary',
      include: [/.*/],
      exlude: [/(\/(en|zh))*\/login/],
    },
  ],
};


export const user =   {
    id: 0,
    username: 'admin',
    password: 'admin',
    permissions: 'admin',
    avatar:  'https://raw.githubusercontent.com/carlomazzaferro/racket/master/docs/images/table-tennis.svg',
};

export const routeList = [
    {
        id: '1',
        icon: 'laptop',
        name: 'Dashboard',
        router: '/dashboard',
    },
];

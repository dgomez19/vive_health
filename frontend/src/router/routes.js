const routes = [
  { path: '/', name: 'login', component: () => import('src/pages/LoginPage.vue') },
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('src/pages/IndexPage.vue') },
      { path: 'users', name: 'users', component: () => import('src/pages/UsersPage.vue') },
      { path: 'patients', name: 'patients', component: () => import('src/pages/PatientsPage.vue') },
      { path: 'specialty', name: 'specialty', component: () => import('src/pages/SpecialtyPage.vue') },
      { path: 'specialist', name: 'specialist', component: () => import('src/pages/SpecialistPage.vue') },
      { path: 'appointment', name: 'appointment', component: () => import('src/pages/AppointmentPage.vue') }
    ]
  },
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes

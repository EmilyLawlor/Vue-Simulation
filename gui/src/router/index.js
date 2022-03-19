import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '../views/Home.vue';
import StopAndWait from '../views/StopAndWait.vue';
import SelectiveRepeat from '../views/SelectiveRepeat.vue';
import GoBackN from '../views/GoBackN.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/stop-and-wait',
    name: 'Stop And Wait',
    component: StopAndWait,
  },
  {
    path: '/selective-repeat',
    name: 'Selective Repeat',
    component: SelectiveRepeat,
  },
  {
    path: '/go-back-n',
    name: 'Go Back N',
    component: GoBackN,
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;

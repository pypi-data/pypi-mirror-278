import {
  notLoggedInValidator,
  hasPersonValidator,
} from "aleksis.core/routeValidators";
import { DateTime } from "luxon";

export default {
  meta: {
    inMenu: true,
    titleKey: "alsijil.menu_title",
    icon: "mdi-account-group-outline",
    iconActive: "mdi-account-group",
    validators: [hasPersonValidator],
  },
  props: {
    byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
  },
  children: [
    {
      path: "extra_marks/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "alsijil.extraMarks",
      meta: {
        inMenu: true,
        titleKey: "alsijil.extra_marks.menu_title",
        icon: "mdi-label-variant-outline",
        iconActive: "mdi-label-variant",
        permission: "alsijil.view_extramarks_rule",
      },
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
    },
    {
      path: "extra_marks/create/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "alsijil.createExtraMark",
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
    },
    {
      path: "extra_marks/:pk(\\d+)/edit/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "alsijil.editExtraMark",
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
    },
    {
      path: "extra_marks/:pk(\\d+)/delete/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "alsijil.deleteExtraMark",
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
    },
    {
      path: "coursebook/",
      component: () => import("./components/coursebook/Coursebook.vue"),
      redirect: () => {
        return {
          name: "alsijil.coursebook",
          params: {
            filterType: "my",
          },
          hash: "#" + DateTime.now().toISODate(),
        };
      },
      name: "alsijil.coursebook_landing",
      props: true,
      meta: {
        inMenu: true,
        icon: "mdi-book-education-outline",
        iconActive: "mdi-book-education",
        titleKey: "alsijil.coursebook.menu_title",
        toolbarTitle: "alsijil.coursebook.menu_title",
        permission: "alsijil.view_documentations_menu_rule",
      },
      children: [
        {
          path: ":filterType(my|all)/:objType(group|course|teacher)?/:objId(\\d+)?/",
          component: () => import("./components/coursebook/Coursebook.vue"),
          name: "alsijil.coursebook",
          meta: {
            titleKey: "alsijil.coursebook.menu_title",
            toolbarTitle: "alsijil.coursebook.menu_title",
            permission: "alsijil.view_documentations_menu_rule",
            fullWidth: true,
          },
        },
      ],
    },
  ],
};

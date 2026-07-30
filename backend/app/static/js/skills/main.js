import {categoryActions} from "./categories.js";
import {skillActions} from './skills.js';

document.addEventListener("alpine:init", () => {
  Alpine.data("adminSkills", () => ({
    categories: [],
    ui: {},
    editingSkillId: null,
    ...categoryActions,
    ...skillActions,

    async init() {
      this.categories = await (await fetch("/skills")).json()
      this.categories.forEach(c => {
        this.ui[c.id] = {open: false, editing: false, editName: ""}
      })
    },
  }));
});

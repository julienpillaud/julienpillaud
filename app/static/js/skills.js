// document.addEventListener("alpine:init", () => {
//   Alpine.data("adminSkills", () => ({
//     categories: [],
//     ui: {},
//     editingSkillId: null,
//     async init() {
//       this.categories = await (await fetch("/skills")).json()
//       // Initialize ui object
//       this.categories.forEach(c => {
//         this.ui[c.id] = {open: false, editing: false, editName: ""}
//       })
//
//       // Save in localStorage for debugging
//       localStorage.setItem("categories", JSON.stringify(this.categories))
//       localStorage.setItem("ui", JSON.stringify(this.ui))
//       this.$watch("categories", (val) => {
//         localStorage.setItem("categories", JSON.stringify(val))
//       }, {deep: true})
//       this.$watch("ui", (val) => {
//         localStorage.setItem("ui", JSON.stringify(val))
//       }, {deep: true})
//     },
//
//
//     // =========================================================================
//     // CATEGORIES
//     // =========================================================================
//     addCategory() {
//       // Add category locally with temporary id
//       const id = `temp_${Date.now()}`
//       this.categories.push({id: id, name: "", skills: []});
//       this.ui[id] = {open: false, editing: true, editName: ""};
//     },
//     // -------------------------------------------------------------------------
//     cancelCategory(category) {
//       // New category with empty name
//       if (category.id.startsWith("temp_") && this.ui[category.id].editName === "") {
//         this._removeCategoryLocal(category);
//         return;
//       }
//
//       this._cancelEditCategory(category);
//     },
//     // -------------------------------------------------------------------------
//     async saveCategory(category) {
//       // New category
//       if (category.id.startsWith("temp_")) {
//
//         // Empty name: cancel
//         if (this.ui[category.id].editName === "") {
//           this._removeCategoryLocal(category);
//           return;
//         }
//
//         // Save category locally
//         category.name = this.ui[category.id].editName;
//         this._cancelEditCategory(category);
//         return;
//       }
//
//       // Existing category
//       // Empty or same name: cancel
//       if (
//         this.ui[category.id].editName === ""
//         || this.ui[category.id].editName === category.name
//       ) {
//         this._cancelEditCategory(category);
//         return;
//       }
//
//       // Backup and save category locally
//       const backup = category.name
//       category.category_name = this.ui[category.id].editName;
//       this._cancelEditCategory(category);
//
//       // Call the backend
//       const response = await fetch("/skills/categories", {
//         method: "PATCH",
//         headers: {"Content-Type": "application/json"},
//         body: JSON.stringify({
//           category_id: category.id,
//           name: category.category_name
//         }),
//       })
//       if (!response.ok) {
//         // Rollback
//         category.category_name = backup
//         showToast("Erreur API !")
//         return;
//       }
//
//       const result = await response.json()
//       showToast(
//         `Catégorie modifiée ! (${result.modified_count} compétences)`,
//         {type: "success"},
//       )
//     },
//     // -------------------------------------------------------------------------
//     async removeCategory(category) {
//       // Backup
//       const backupCategories = [...this.categories]
//       const backupUi = {...this.ui}
//
//       // Remove the category from data
//       this._removeCategoryLocal(category)
//
//       // Call the backend
//       const response = await fetch(`/skills/categories/${category.id}`, {
//         method: "DELETE",
//         headers: {"Content-Type": "application/json"},
//       })
//       if (!response.ok) {
//         // Rollback
//         this.categories = backupCategories
//         this.ui = backupUi
//         showToast("Erreur API !")
//         return;
//       }
//
//       showToast("Catégorie supprimée !", {type: "success"})
//     },
//     // -------------------------------------------------------------------------
//     openCategory(category) {
//       this.ui[category.id].open = !this.ui[category.id].open;
//     },
//     // -------------------------------------------------------------------------
//     editCategory(category) {
//       this.ui[category.id].editing = true;
//       this.ui[category.id].editName = category.name;
//     },
//     // -------------------------------------------------------------------------
//     sortCategories(itemId, newIndex) {
//       const moved = this.categories.find(c => c.id === itemId)
//       this.categories.splice(this.categories.indexOf(moved), 1)
//       this.categories.splice(newIndex, 0, moved)
//     },
//     // -------------------------------------------------------------------------
//     _removeCategoryLocal(category) {
//       this.categories = this.categories.filter(s => s.id !== category.id);
//       delete this.ui[category.id];
//     },
//     _cancelEditCategory(category) {
//       this.ui[category.id].editing = false;
//       this.ui[category.id].editName = "";
//     },
//
//
//     // =========================================================================
//     // SKILLS
//     // =========================================================================
//     addSkill(category) {
//       // Add skill locally with temporary id
//       const id = `temp_${Date.now()}`
//       category.skills.push({id: id, name: ""})
//       this.editingSkillId = id
//     },
//     // -------------------------------------------------------------------------
//     async saveSkill(category, skill) {
//       // If empty name, remove skill from category
//       if (skill.name === "") {
//         category.skills = category.skills.filter(s => s.id !== skill.id);
//         this.editingSkillId = null;
//         return;
//       }
//
//       // Cancel editing
//       this.editingSkillId = null;
//
//       // Call the backend
//       const payload = {
//         category: {
//           // Remove temporary id
//           id: category.id.startsWith("temp_") ? null : category.id,
//           name: category.name,
//           display_order: this.categories.indexOf(category),
//         },
//         name: skill.name,
//         display_order: category.skills.indexOf(skill),
//       }
//       const response = await fetch("/skills", {
//         method: "POST",
//         headers: {"Content-Type": "application/json"},
//         body: JSON.stringify(payload)
//       })
//       if (!response.ok) {
//         showToast("Erreur API !")
//         this._removeSkillLocal(category, skill)
//         return;
//       }
//       const newSkill = await response.json()
//
//       // Update the category and skill id
//       if (category.id.startsWith("temp_")) {
//         category.id = newSkill.category.id
//         this.ui[category.id] = {open: false, editing: false, editName: ""}
//       }
//       skill.id = newSkill.id
//
//       showToast("Compétence créée", {type: "success"})
//     },
//     // -------------------------------------------------------------------------
//     async removeSkill(category, skill) {
//       // Backup
//       const backupCategories = [...this.categories]
//       const backupUi = {...this.ui}
//
//       this._removeSkillLocal(category, skill)
//
//       // Call the backend
//       const response = await fetch(`/skills/${skill.id}`, {
//         method: "DELETE",
//         headers: {"Content-Type": "application/json"},
//       })
//       if (!response.ok) {
//         // Rollback
//         this.categories = backupCategories
//         this.ui = backupUi
//         showToast("Erreur API !")
//         return;
//       }
//
//       showToast("Compétence supprimée !", {type: "success"})
//     },
//     // -------------------------------------------------------------------------
//     _removeSkillLocal(category, skill) {
//       // Remove skill from category
//       category.skills = category.skills.filter(s => s.id !== skill.id);
//
//       // If empty, remove category
//       if (category.skills.length === 0) {
//         this.categories = this.categories.filter(c => c.id !== category.id);
//       }
//     },
//     // -------------------------------------------------------------------------
//     sortSkills(itemId, newIndex) {
//       const category = this.categories.find(c => c.skills.find(s => s.id === itemId));
//       const moved = category.skills.find(s => s.id === itemId);
//       category.skills.splice(category.skills.indexOf(moved), 1);
//       category.skills.splice(newIndex, 0, moved);
//     },
//     // -------------------------------------------------------------------------
//   }))
// })

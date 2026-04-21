document.addEventListener("alpine:init", () => {
  Alpine.data("resumeSkills", () => ({
    skills: [],
    newCategoryName: "",
    newSkillName: "",
    updateSkillTimer: null,
    // -------------------------------------------------------------------------
    async init() {
      this.skills = await (await fetch("/skills")).json()
    },
    // -------------------------------------------------------------------------
    addCategory() {
      if (!this.newCategoryName) {
        showToast("Entrer un nom de catégorie !", {type: "warning"})
        return
      }
      this.skills.push({
        id: `temp_${Date.now()}`,
        category_name: this.newCategoryName,
        skills: [],
      })
      this.newCategoryName = ""
    },
    // -------------------------------------------------------------------------
    async removeCategory(categoryId) {
      // Remove the category
      this.skills = this.skills.filter(s => s.id !== categoryId)

      // Call the backend
      const response = await fetch(`/skills/categories/${categoryId}`, {
        method: 'DELETE',
        headers: {'Content-Type': 'application/json'},
      })
      if (!response.ok) {
        showToast("Erreur API !")
        return;
      }

      showToast("Catégorie supprimée !", {type: "success"})
    },
    // -------------------------------------------------------------------------
    async addSkill(categoryId) {
      const newSkillName = this.newSkillName
      if (!newSkillName) {
        showToast("Entrer un nom !", {type: "warning"})
        return;
      }

      // Add the new skill
      const skillGroup = this.skills.find(s => s.id === categoryId)
      const categoryDisplayOrder = this.skills.findIndex(s => s.id === categoryId) + 1
      const tempId = `temp_${Date.now()}`

      skillGroup.skills.push({id: tempId, name: newSkillName})
      this.newSkillName = ""

      // Call the backend
      const data = {
        category: {
          id: categoryId.startsWith('temp_') ? null : categoryId,
          name: skillGroup.category_name,
          display_order: categoryDisplayOrder,
        },
        name: newSkillName,
        display_order: skillGroup.skills.length,
      }
      const response = await fetch("/skills", {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
      })
      if (!response.ok) {
        showToast("Erreur API !")
        return;
      }
      const newSkill = await response.json()

      // Update the category and skill id
      if (categoryId.startsWith('temp_')) {
        skillGroup.id = newSkill.category.id
      }

      const skill = skillGroup.skills.find(s => s.id === tempId)
      skill.id = newSkill.id

      showToast("Compétence créée", {type: "success"})
    },
    // -------------------------------------------------------------------------
    async updateSkill(categoryId, skillId,) {
      clearTimeout(this.updateSkillTimer)
      this.updateSkillTimer = setTimeout(async () => {
        const skillGroup = this.skills.find(s => s.id === categoryId)
        const skill = skillGroup.skills.find(s => s.id === skillId)

        await fetch(`/skills/${skillId}`, {
          method: 'PATCH',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({name: skill.name})
        })
      }, 500)
    },
    // -------------------------------------------------------------------------
    async removeSkill(categoryId, skillId) {
      // Remove the skill
      const skillGroup = this.skills.find(s => s.id === categoryId)
      skillGroup.skills = skillGroup.skills.filter(s => s.id !== skillId)

      // Call the backend
      const response = await fetch(`/skills/${skillId}`, {
        method: 'DELETE',
        headers: {'Content-Type': 'application/json'},
      })
      if (!response.ok) {
        showToast("Erreur API !")
        return;
      }

      if (skillGroup.skills.length === 0) {
        this.skills = this.skills.filter(s => s.id !== categoryId)
      }

      showToast("Compétence supprimée !", {type: "success"})
    },
    // -------------------------------------------------------------------------
  }))
})

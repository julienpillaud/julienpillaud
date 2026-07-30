export const skillActions = {
  // ---------------------------------------------------------------------------
  addSkill(category) {
    // Add skill locally with temporary id
    const id = `temp_${Date.now()}`
    category.skills.push({id: id, name: ""})
    this.editingSkillId = id
  },
  // ---------------------------------------------------------------------------
  async saveSkill(category, skill) {
    // If empty name, remove skill from category
    if (skill.name === "") {
      this._removeSkillLocal(category, skill)
      return;
    }

    // Cancel editing
    this.editingSkillId = null;

    // Call the backend
    const response = await createSkill(this, category, skill);
    if (!response.ok) {
      showToast("Erreur API !")
      this._removeSkillLocal(category, skill)
      return;
    }
    const newSkill = await response.json()

    // Update the category and skill id
    if (category.id.startsWith("temp_")) {
      category.id = newSkill.category_id
      this.ui[category.id] = {open: true, editing: false, editName: ""}
    }
    skill.id = newSkill.id

    showToast("Compétence créée", {type: "success"})
  },
  // ---------------------------------------------------------------------------
  async removeSkill(category, skill) {
    // Call the backend
    const response = await deleteSkill(skill)
    if (!response.ok) {
      showToast("Erreur API !")
      return;
    }

    this._removeSkillLocal(category, skill)
    showToast("Compétence supprimée !", {type: "success"})
  },
  // ---------------------------------------------------------------------------
  sortSkills(itemId, newIndex) {
    const category = this.categories.find(c => c.skills.find(s => s.id === itemId));
    const moved = category.skills.find(s => s.id === itemId);
    category.skills.splice(category.skills.indexOf(moved), 1);
    category.skills.splice(newIndex, 0, moved);

    const response = reorderSkills(category.skills)
  },
  // ---------------------------------------------------------------------------
  _removeSkillLocal(category, skill) {
    // Remove skill from category
    category.skills = category.skills.filter(s => s.id !== skill.id);

    // If empty, remove category
    if (category.skills.length === 0) {
      this.categories = this.categories.filter(c => c.id !== category.id);
    }
  },
  // ---------------------------------------------------------------------------
}

// =============================================================================
// API
// =============================================================================
async function createSkill(component, category, skill) {
  const payload = {
    category: {
      // Remove temporary id
      id: category.id.startsWith("temp_") ? null : category.id,
      name: category.name,
      display_order: component.categories.indexOf(category),
    },
    name: skill.name,
    display_order: category.skills.indexOf(skill),
  }

  return await fetch("/skills", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(payload)
  })
}

// -----------------------------------------------------------------------------
async function deleteSkill(skill) {
  return await fetch(`/skills/${skill.id}`, {
    method: "DELETE",
    headers: {"Content-Type": "application/json"},
  })
}

// -----------------------------------------------------------------------------
async function reorderSkills(skills) {
  const payload = skills.map((skill, index) => ({
    id: skill.id,
    display_order: index
  }))

  return await fetch("/skills/reorder", {
    method: "PATCH",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(payload)
  })
}

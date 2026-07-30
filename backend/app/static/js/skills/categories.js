export const categoryActions = {
  // ---------------------------------------------------------------------------
  openCategory(category) {
    this.ui[category.id].open = !this.ui[category.id].open;
  },
  // ---------------------------------------------------------------------------
  editCategory(category) {
    this.ui[category.id].editing = true;
    this.ui[category.id].editName = category.name;
  },
  // ---------------------------------------------------------------------------
  addCategory() {
    // Add category locally with temporary id
    const id = `temp_${Date.now()}`
    this.categories.push({id: id, name: "", skills: []});
    this.ui[id] = {open: false, editing: true, editName: ""};
  },
  // ---------------------------------------------------------------------------
  cancelCategory(category) {
    // New category with empty name
    if (category.id.startsWith("temp_") && this.ui[category.id].editName === "") {
      this._removeCategoryLocal(category);
      return;
    }

    this._cancelEditCategory(category);
  },
  // ---------------------------------------------------------------------------
  async saveCategory(category) {
    // New category
    if (category.id.startsWith("temp_")) {

      // Empty name: cancel
      if (this.ui[category.id].editName === "") {
        this._removeCategoryLocal(category);
        return;
      }

      // Save category locally
      category.name = this.ui[category.id].editName;
      this._cancelEditCategory(category);
      this.ui[category.id].open = true;
      return;
    }

    // Edit existing category name
    // Empty or same name: cancel
    if (
      this.ui[category.id].editName === ""
      || this.ui[category.id].editName === category.name
    ) {
      this._cancelEditCategory(category);
      return;
    }

    // Backup
    const backup = category.name
    // Save category locally
    category.name = this.ui[category.id].editName;
    this._cancelEditCategory(category);

    // Call the backend
    const response = await updateCategory(category);
    if (!response.ok) {
      // Rollback
      category.category_name = backup
      showToast("Erreur API !")
      return;
    }

    showToast("Catégorie modifiée !", {type: "success"})
  },
  // ---------------------------------------------------------------------------
  async removeCategory(category) {
    this._removeCategoryLocal(category)

    const response = await deleteCategory(category);
    if (!response.ok) {
      showToast("Erreur API !")
      return;
    }

    showToast("Catégorie supprimée !", {type: "success"})
  },
  // ---------------------------------------------------------------------------
  async sortCategories(itemId, newIndex) {
    const moved = this.categories.find(c => c.id === itemId)
    this.categories.splice(this.categories.indexOf(moved), 1)
    this.categories.splice(newIndex, 0, moved)

    const response = await reorderCategories(this)
    if (!response.ok) {
      showToast("Erreur API !")
    }
  },
  // ---------------------------------------------------------------------------
  _removeCategoryLocal(category) {
    this.categories = this.categories.filter(s => s.id !== category.id);
    delete this.ui[category.id];
  },
  // ---------------------------------------------------------------------------
  _cancelEditCategory(category) {
    this.ui[category.id].editing = false;
    this.ui[category.id].editName = "";
  },
  // ---------------------------------------------------------------------------
}

// =============================================================================
// API
// =============================================================================
async function updateCategory(category) {
  const payload = {name: category.name}

  return await fetch(`/skills/categories/${category.id}`, {
    method: "PATCH",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(payload)
  })
}

// -----------------------------------------------------------------------------
async function deleteCategory(category) {
  return await fetch(`/skills/categories/${category.id}`, {
    method: "DELETE",
    headers: {"Content-Type": "application/json"},
  })
}

// -----------------------------------------------------------------------------
async function reorderCategories(component) {
  const payload = component.categories.map((category, index) => ({
    id: category.id,
    display_order: index
  }))

  return await fetch("/skills/categories/reorder", {
    method: "PATCH",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(payload)
  })
}

export interface ContactInfo {
  full_name: string
  job_title: string
  email: string
  github_username: string
  linkedin_username: string
  available: boolean
  location: string
  remote: string
}

export interface Education {
  year: number
  name: string
  school: string
}

export interface Language {
  display_order: number
  name: string
  level: string
  optional: boolean
}

export interface Metadata {
  contact: ContactInfo
  education: Education[]
  languages: Language[]
}

export interface Skill {
  name: string
}

export interface SkillCategory {
  name: string
  skills: Skill[]
}

export interface Task {
  label: string
  details: string[]
}

export interface Project {
  context: string
  tasks: Task[]
}

export interface Experience {
  company: string
  role: string
  period: string
  projects: Project[]
}

export interface Resume {
  metadata: Metadata
  skills: SkillCategory[]
  experiences: Experience[]
}

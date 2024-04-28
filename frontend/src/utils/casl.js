import { ROLE_ADMINISTRATOR } from 'src/constants/users'
import { ALL_MODULES, CRUD_ACTION } from 'src/constants/permissions'
import { AbilityBuilder } from '@casl/ability'

const withoutPermissions = { skills: [] }

const permissions = [
  {
    role: ROLE_ADMINISTRATOR,
    skills: [{ module: ALL_MODULES, actions: [CRUD_ACTION] }]
  }
]

export const definePermissions = user => {
  const { can, rules } = new AbilityBuilder()

  const permission = permissions.find(permission => permission.role === ({ ...user.role }).code) || withoutPermissions

  permission.skills.forEach(skill => can(skill.actions, skill.module))

  return rules
}

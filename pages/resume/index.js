import Header from '../../components/header'
import StyleClass from '../../libs/styleutil'
import style from '../../styles/style.module.css'
import { getAsset, Resume } from '../../libs/assets'

const Skills = () => {

  const SkillCategory = (category, i) => {

    const SkillsList = (skill) => {
      if (skill.attributes.length > 0) {
        return `${skill.name} (${skill.attributes.join(', ')})`;
      } else {
        return skill.name;
      }
    }

    return (
      <div id={i}>
        <p><b>{category.name}</b> {getAsset(category.values).map(SkillsList).join(', ')}</p>
      </div>
    )
  }
  return (
    <div className={StyleClass(style.section)}>
      <h1>Skills</h1>
      {getAsset(Resume.skills).map(SkillCategory)}
    </div>
  )
};

export default function Home() {
  return (
    <div>
      <Header path={
        ["Resume"]
      } />
      <center>
        <h1 className={StyleClass(style.section, style.header1)}>{Resume.name}</h1>
        {Skills()}
      </center>
    </div>
  )
}
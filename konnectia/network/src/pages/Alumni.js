import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

const Alumni = () => {
  const [alumni, setAlumni] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedDepartment, setSelectedDepartment] = useState('all');
  const [selectedYear, setSelectedYear] = useState('all');

  useEffect(() => {
    fetchAlumni();
  }, []);

  const fetchAlumni = () => {
    // Simulated alumni data
    setAlumni([
      {
        id: 1,
        name: 'Sarah Johnson',
        position: 'Software Engineer at Google',
        avatar: 'https://via.placeholder.com/150',
        department: 'Computer Science',
        graduationYear: '2020',
        company: 'Google',
        location: 'Mountain View, CA',
        bio: 'Passionate about AI and Machine Learning',
        skills: ['JavaScript', 'Python', 'Machine Learning'],
        isFollowing: false
      },
      {
        id: 2,
        name: 'David Chen',
        position: 'Product Manager at Microsoft',
        avatar: 'https://via.placeholder.com/150',
        department: 'Computer Science',
        graduationYear: '2019',
        company: 'Microsoft',
        location: 'Seattle, WA',
        bio: 'Product enthusiast with a focus on user experience',
        skills: ['Product Management', 'UX Design', 'Agile'],
        isFollowing: true
      },
      {
        id: 3,
        name: 'Emily Brown',
        position: 'Data Scientist at Amazon',
        avatar: 'https://via.placeholder.com/150',
        department: 'Data Science',
        graduationYear: '2021',
        company: 'Amazon',
        location: 'Seattle, WA',
        bio: 'Data-driven problem solver',
        skills: ['Python', 'R', 'SQL', 'Machine Learning'],
        isFollowing: false
      }
    ]);
  };

  const handleFollow = (alumniId) => {
    setAlumni(alumni.map(alum => 
      alum.id === alumniId 
        ? { ...alum, isFollowing: !alum.isFollowing }
        : alum
    ));
  };

  const filteredAlumni = alumni.filter(alum => {
    const matchesSearch = alum.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         alum.position.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         alum.company.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesDepartment = selectedDepartment === 'all' || alum.department === selectedDepartment;
    const matchesYear = selectedYear === 'all' || alum.graduationYear === selectedYear;
    
    return matchesSearch && matchesDepartment && matchesYear;
  });

  const departments = ['all', ...new Set(alumni.map(alum => alum.department))];
  const years = ['all', ...new Set(alumni.map(alum => alum.graduationYear))];

  return (
    <div className="alumni-container">
      <div className="alumni-header">
        <h1 className="alumni-title">Alumni Directory</h1>
        <div className="alumni-search">
          <input
            type="text"
            placeholder="Search by name, position, or company..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="alumni-search-input"
          />
          <select
            value={selectedDepartment}
            onChange={(e) => setSelectedDepartment(e.target.value)}
            className="alumni-search-select"
          >
            {departments.map(dept => (
              <option key={dept} value={dept}>
                {dept === 'all' ? 'All Departments' : dept}
              </option>
            ))}
          </select>
          <select
            value={selectedYear}
            onChange={(e) => setSelectedYear(e.target.value)}
            className="alumni-search-select"
          >
            {years.map(year => (
              <option key={year} value={year}>
                {year === 'all' ? 'All Years' : `Class of ${year}`}
              </option>
            ))}
          </select>
        </div>
      </div>
      <div className="alumni-grid">
        {filteredAlumni.map((alum) => (
          <div key={alum.id} className="alumni-card">
            <div className="alumni-card-header">
              <img
                src={alum.avatar}
                alt={alum.name}
                className="alumni-card-avatar"
              />
              <div className="alumni-card-details">
                <h3 className="alumni-card-name">{alum.name}</h3>
                <p className="alumni-card-position">{alum.position}</p>
                <p className="alumni-card-meta">
                  {alum.department} • Class of {alum.graduationYear}
                </p>
              </div>
            </div>
            <div className="alumni-card-bio">{alum.bio}</div>
            <div className="alumni-card-company-location">
              <span className="alumni-card-company">Company: {alum.company}</span>
              <span className="alumni-card-location">Location: {alum.location}</span>
            </div>
            <div className="alumni-card-skills">
              <span className="alumni-card-skills-title">Skills:</span>
              <div className="alumni-card-skill-list">
                {alum.skills.map((skill, index) => (
                  <span key={index} className="alumni-card-skill">
                    {skill}
                  </span>
                ))}
              </div>
            </div>
            <div className="alumni-card-actions">
              <Link
                to={`/profile/${alum.id}`}
                className="alumni-card-view-profile"
              >
                View Profile
              </Link>
              <button
                onClick={() => handleFollow(alum.id)}
                className={`alumni-card-follow-btn${alum.isFollowing ? ' following' : ''}`}
              >
                {alum.isFollowing ? 'Following' : 'Follow'}
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Alumni; 
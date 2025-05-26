import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

const Profile = () => {
  const { userId } = useParams();
  const [profile, setProfile] = useState(null);
  const [posts, setPosts] = useState([]);
  const [isFollowing, setIsFollowing] = useState(false);
  const [followersCount, setFollowersCount] = useState(0);

  useEffect(() => {
    fetchProfile();
    fetchUserPosts();
  }, [userId]);

  const fetchProfile = async () => {
    // TODO: Replace with actual API call
    setProfile({
      id: userId,
      name: 'John Doe',
      avatar: 'https://via.placeholder.com/150',
      bio: 'Computer Science Student',
      department: 'Computer Science',
      graduationYear: '2024',
      followers: 120,
      following: 85,
      isAlumni: false,
      currentPosition: 'Student',
      interests: ['Web Development', 'AI', 'Machine Learning'],
      skills: ['JavaScript', 'React', 'Node.js', 'Python']
    });
  };

  const fetchUserPosts = async () => {
    // TODO: Replace with actual API call
    setPosts([
      {
        id: 1,
        content: 'Just finished my final project!',
        likes: 15,
        comments: 5,
        timestamp: '2 hours ago'
      },
      {
        id: 2,
        content: 'Excited about the upcoming hackathon!',
        likes: 8,
        comments: 3,
        timestamp: '1 day ago'
      }
    ]);
  };

  const handleFollow = async () => {
    // TODO: Implement follow functionality
    setIsFollowing(!isFollowing);
    setFollowersCount(prev => isFollowing ? prev - 1 : prev + 1);
  };

  return (
    <div className="profile-container">
      <div className="profile-header">
        <img
          src={profile?.avatar}
          alt={profile?.name}
          className="profile-avatar-large"
        />
        <div className="profile-details">
          <h1 className="profile-name-large">{profile?.name}</h1>
          <p className="profile-bio">{profile?.bio}</p>
          <p className="profile-meta">
            {profile?.department} • Class of {profile?.graduationYear}
          </p>
          <button
            onClick={handleFollow}
            className={`profile-follow-btn${isFollowing ? ' following' : ''}`}
          >
            {isFollowing ? 'Following' : 'Follow'}
          </button>
          <div className="profile-stats">
            <div>
              <span className="profile-stat-number">{followersCount}</span>
              <span className="profile-stat-label">Followers</span>
            </div>
            <div>
              <span className="profile-stat-number">{profile?.following}</span>
              <span className="profile-stat-label">Following</span>
            </div>
          </div>
          {profile?.isAlumni && (
            <div className="profile-current-position">
              Current Position: {profile?.currentPosition}
            </div>
          )}
        </div>
      </div>
      <div className="profile-skills-interests">
        <div className="profile-skills">
          <h3>Skills</h3>
          <div className="profile-skill-list">
            {profile?.skills.map((skill, index) => (
              <span key={index} className="profile-skill">
                {skill}
              </span>
            ))}
          </div>
        </div>
        <div className="profile-interests">
          <h3>Interests</h3>
          <div className="profile-interest-list">
            {profile?.interests.map((interest, index) => (
              <span key={index} className="profile-interest">
                {interest}
              </span>
            ))}
          </div>
        </div>
      </div>
      <div className="profile-posts">
        <h2 className="profile-posts-title">Posts</h2>
        {posts.map((post) => (
          <div key={post.id} className="profile-post">
            <p className="profile-post-content">{post.content}</p>
            <div className="profile-post-actions">
              <span className="profile-post-like">❤️ {post.likes}</span>
              <span className="profile-post-comment">💬 {post.comments}</span>
              <span className="profile-post-timestamp">{post.timestamp}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Profile; 
import React, { useState, useEffect } from 'react';

const Dashboard = () => {
  const [posts, setPosts] = useState([]);
  const [alumni, setAlumni] = useState([]);
  const [userProfile, setUserProfile] = useState(null);
  const [newPost, setNewPost] = useState('');

  useEffect(() => {
    fetchUserProfile();
    fetchPosts();
    fetchAlumniSuggestions();
  }, []);

  const fetchUserProfile = () => {
    setUserProfile({
      name: 'John Doe',
      avatar: 'https://via.placeholder.com/150',
      followers: 120,
      following: 85,
      bio: 'Computer Science Student',
      department: 'Computer Science',
      graduationYear: '2024'
    });
  };

  const fetchPosts = () => {
    setPosts([
      {
        id: 1,
        author: 'Jane Smith',
        authorAvatar: 'https://via.placeholder.com/40',
        content: 'Just finished my final project!',
        likes: 15,
        comments: 5,
        timestamp: '2 hours ago'
      },
      {
        id: 2,
        author: 'Mike Johnson',
        authorAvatar: 'https://via.placeholder.com/40',
        content: 'Excited about the upcoming hackathon!',
        likes: 8,
        comments: 3,
        timestamp: '1 day ago'
      }
    ]);
  };

  const fetchAlumniSuggestions = () => {
    setAlumni([
      {
        id: 1,
        name: 'Sarah Johnson',
        position: 'Software Engineer at Google',
        avatar: 'https://via.placeholder.com/50',
        department: 'Computer Science',
        graduationYear: '2020',
        isFollowing: false
      },
      {
        id: 2,
        name: 'David Chen',
        position: 'Product Manager at Microsoft',
        avatar: 'https://via.placeholder.com/50',
        department: 'Computer Science',
        graduationYear: '2019',
        isFollowing: false
      }
    ]);
  };

  const handleCreatePost = (e) => {
    e.preventDefault();
    if (!newPost.trim()) return;
    const post = {
      id: Date.now(),
      author: userProfile.name,
      authorAvatar: userProfile.avatar,
      content: newPost,
      likes: 0,
      comments: 0,
      timestamp: 'Just now'
    };
    setPosts([post, ...posts]);
    setNewPost('');
  };

  const handleLike = (postId) => {
    setPosts(posts.map(post => 
      post.id === postId 
        ? { ...post, likes: post.likes + 1 }
        : post
    ));
  };

  const handleFollow = (alumniId) => {
    setAlumni(alumni.map(alum => 
      alum.id === alumniId 
        ? { ...alum, isFollowing: !alum.isFollowing }
        : alum
    ));
  };

  return (
    <div className="dashboard-container">
      <div className="sidebar profile-sidebar">
        <div className="profile-overview">
          <img
            src={userProfile?.avatar}
            alt={userProfile?.name}
            className="profile-avatar"
          />
          <h2 className="profile-name">{userProfile?.name}</h2>
          <p className="profile-bio">{userProfile?.bio}</p>
          <div className="profile-stats">
            <div>
              <p className="profile-stat-number">{userProfile?.followers}</p>
              <p className="profile-stat-label">Followers</p>
            </div>
            <div>
              <p className="profile-stat-number">{userProfile?.following}</p>
              <p className="profile-stat-label">Following</p>
            </div>
          </div>
        </div>
      </div>

      <div className="feed">
        <div className="create-post">
          <form onSubmit={handleCreatePost}>
            <textarea
              value={newPost}
              onChange={(e) => setNewPost(e.target.value)}
              placeholder="What's on your mind?"
              className="create-post-textarea"
              rows="3"
            />
            <button type="submit" className="create-post-btn">Post</button>
          </form>
        </div>
        <div className="posts-feed">
          {posts.map((post) => (
            <div key={post.id} className="post">
              <div className="post-header">
                <img
                  src={post.authorAvatar}
                  alt={post.author}
                  className="post-author-avatar"
                />
                <div>
                  <h3 className="post-author">{post.author}</h3>
                  <p className="post-timestamp">{post.timestamp}</p>
                </div>
              </div>
              <p className="post-content">{post.content}</p>
              <div className="post-actions">
                <button onClick={() => handleLike(post.id)} className="like-btn">
                  ❤️ {post.likes}
                </button>
                <button className="comment-btn">
                  💬 {post.comments}
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="sidebar alumni-suggestions">
        <h3 className="alumni-title">Alumni Suggestions</h3>
        <div className="alumni-list">
          {alumni.map((alum) => (
            <div key={alum.id} className="alumni-card">
              <div className="alumni-info">
                <img
                  src={alum.avatar}
                  alt={alum.name}
                  className="alumni-avatar"
                />
                <div>
                  <h4 className="alumni-name">{alum.name}</h4>
                  <p className="alumni-position">{alum.position}</p>
                  <p className="alumni-meta">
                    {alum.department} • Class of {alum.graduationYear}
                  </p>
                </div>
              </div>
              <button
                onClick={() => handleFollow(alum.id)}
                className={`follow-btn${alum.isFollowing ? ' following' : ''}`}
              >
                {alum.isFollowing ? 'Following' : 'Follow'}
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Dashboard; 
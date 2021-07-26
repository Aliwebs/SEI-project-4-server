# [Postbook](https://elated-williams-fb7045.netlify.app/)

Frontend [here](https://github.com/Aliwebs/SEI-project-4-client)

## Summary

This was a full stack application made with a React frontend and with a Django backend. This is a social media clone, a lot of inspiration was taken from Twitter and Facebook. The main goal was to get all the basic functions of a social media app within the timeframe of this project, which was a little over a week.

## Brief

- Build a full-stack **application** by making your own backend and your own front-end.
- Use a Python Django API using Django REST Framework to serve your data from a Postgres database.
- Consume your API with a **separate** front-end built with React.
- Be a complete product which most likely means multiple relationships and CRUD functionality for at least a couple of models.
- Implement thoughtful user **stories/wireframes** that are significant enough to help you know which features are core MVP and which you can cut.
- Have a visually impressive design to kick your portfolio up a notch and have something to wow future clients & employers.**ALLOW** time for this.
- Be deployed **online** so it's publicly accessible.

## Table of contents

- [Postbook](#postbook)
  - [Summary](#summary)
  - [Brief](#brief)
  - [Table of contents](#table-of-contents)
  - [Technologies Used](#technologies-used)
  - [Approach Taken](#approach-taken)
    - [Backend](#backend)
    - [Frontend](#frontend)
  - [Screenshots](#screenshots)
  - [Bugs](#bugs)
  - [Future Features](#future-features)
  - [Wins](#wins)
  - [Challenges](#challenges)
  - [Key Learnings](#key-learnings)

## Technologies Used

- HTML5
- SASS
- JavaScript
- React
- Django
- Python
- PostgreSQL
- Git & Github
- Heroku
- Netlify

## Approach Taken

I planned most of the designs and features in Excalidraw first, this helped a lot during the project as I had something to reference back to. I had a list of features that I wanted as MVP and as stretch goals and I kinda just ticked them off one by one.

### Backend

I started by making an ERD diagram for my database models. The general idea is that each post has an owner and that is the user who made the post, attachments and comments have a post id to reference which post they belong to. Some of the tables in the diagram were not created as they were part of stretch goals I could not get to.
![ERD diagram](./readme-assets/ERD.png)

Then I wrote the models for the post object and all the other models, I have put the post model below as an example.

```python
class Post(models.Model):
   content = models.TextField(max_length=250)
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(null=True, auto_now=True)
   user = models.ForeignKey(
       'jwt_auth.User',
       related_name='posts',
       on_delete=models.CASCADE
   )
   liked_by = models.ManyToManyField(
       'jwt_auth.User',
       blank=True
   )
 
   def __str__(self):
       return f'{self.content}'
```

Also the serializers for the post object.

### Frontend

The first thing I did for the frontend in this project was to get the user data in `App.js` everytime the page refreshes or the `updateProfile` function is called. This was so the navigation bar which had the username and profile could be up to date. Apart from that the profile page uses the data passed down by `App.js` to render the user profile IF the profile you are trying to see belongs to you the user. If the profile belongs to another user the `Profile.js` component makes another API call to get that user's data.

```javascript
 
const { pathname } = useLocation()
 
 useEffect(() => {
   const token = localStorage.getItem('token')
   if (token) {
     getProfile()
       .then(res => setProfile(res.data))
       .catch(err => console.log(err.response))
   }
 }, [pathname])
 
 const updateProfile = (user) => {
   if (localStorage.getItem('token')) {
     getProfile(user.id)
       .then(res => setProfile(res.data))
       .catch(err => console.log(err.response))
   }
 }
 
```

The use effect below does the check for the user checking their own profile or another one etc.

```javascript
 
 useEffect(() => {
   if (!profile && !id) return
 
   if (id) {
     getProfile(id)
       .then(res => setFormData(res.data))
       .then(() => {
         return getPosts(id)
       })
       .then(res => setPosts(res.data))
       .catch((err) => console.log(err))
   } else {
     setFormData(profile)
     getPosts(userId)
       .then(res => setPosts(res.data))
       .catch((err) => console.log(err))
   }
 }, [profile, setFormData, id, userId])
 
```

The `Home.js` has most of the content on the website, it gets the data for all the posts and renders the `PostCard.js` component for each post. In the `PostCard.js` there are two things being rendered `ProfileCard.js` and the comments, also comments data for each post is fetched inside the `PostCard.js` component.

```HTML
 
 <div id="posts">
   {posts && posts.map(post => (
     <PostCard key={post.id} {...post} updateData={updateData} setUpdateData={setUpdateData} />
   ))}
 </div>
 
```

```javascript
 
const handleSubmit = (e) => {
   e.preventDefault()
 
   postComment(id, formdata)
     .then((res) => {
       handleChange({ target: { name: 'content', value: '' } })
       setCommentsData([res.data, ...commentsData])
     })
     .catch(err => console.log(err?.response.data))
 }
 
 const handleDelete = ({ target: { value } }) => {
   if (window.confirm('Do you really want to delete this comment?')) {
     deleteComment(value)
       .then(() => {
         setCommentsData([...comments.filter(comment => comment.id !== Number(value))])
       })
       .catch(err => console.log(err?.response.data))
   }
 }
 
```

```HTML
<div>
 {comments && comments.map(comment => (
   <div key={comment.id} className="comment">
     {userId === comment.owner.id &&
       <button className="close" onTouchEnd={handleDelete} onClick={handleDelete} value={comment.id}>X</button>}
     <ProfileCard {...comment.owner} hideUsername={true} />
     <div>
       <p >{comment.content}</p>
       <small className="timestamp"><Moment fromNow>{comment.createdAt}</Moment></small>
     </div>
   </div>
 ))}
</div>
 
```

There is also a sorting function that sorts comments by date. Posts are sorted in the backend.

```javascript
 
comments = commentsData?.sort((a, b) => {
   return new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
 })
 
```

```python
 
def get(self, _request):
       posts = Post.objects.all().order_by('-created_at')
       serialized_posts = PopulatedPostSerializer(posts, many=True)
       return Response(serialized_posts.data)
 
```

## Screenshots

Login
![Login](./readme-assets/login.PNG)
Register
![Register](./readme-assets/register.PNG)
Home
![home](./readme-assets/home.PNG)
Profile
![Profile](./readme-assets/profile.PNG)

## Bugs

- When a logged out user is not taken to the login page, instead it goes to a blank page and the page needs to be refreshed. This bug was related to react component unmount which I could not solve until the end of the project.
- Like counters will bug out sometimes.

## Future Features

- Add a page for you.
- Remove posts made by the user from the feed.
- Add messaging.
- Improve the user journey.

## Wins

- Getting the project to my MVP was a big win.
- Implementing the user icon component with optional things was a big win, it saved a lot of time and repeated code.

## Challenges

After using Bulma in the previous projects, one of the biggest challenges was making the styles for this project in just CSS. I had a lot of trouble especially with the small components that needed specific positioning. But overall I learned a lot about CSS by doing so.
Not as big of a challenge but I had some trouble making the relationships with models in the backend.

## Key Learnings

I learnt a lot during this project as it was my first solo full stack project. Working solo I had a lot more flexibility when making decisions and although I started out with estimates for the project to get to the MVP stage in 4 days it took a lot longer than expected. This was mainly due to the fact that I had used bulma in the last 2 projects and writing just CSS again took some time alongside other issues I faced in the backend. Overall I learnt the importance of having a project timeline and a clear plan with daily tasks which I did not use.

import { Container } from 'react-bootstrap'
import { BrowserRouter as Router, Route } from 'react-router-dom'

// Components
import Header from './components/Header';
import Footer from './components/Footer';

// Site Pages/Screens
import HomeScreen from './screens/HomeScreen';

function App() {
  return (
    <Router>
      <Header/>
      <main>
        <Container>
          <Route path='/' component={HomeScreen} exact />
        </Container>
      </main>
      <Footer/>
    </Router>
  );
}

export default App;

import { React, useState } from 'react'
import { Navbar, Container, Nav, Image, Offcanvas } from 'react-bootstrap'
import { LinkContainer } from 'react-router-bootstrap'
import logo from '../images/logo.png';


function Header() {
    const [ show, setShow ] = useState(false);

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    return (
        <>
            <Navbar collapseOnSelect expand="lg" bg="light" variant="light" expanded={false} className="shadow-sm">
                <Container>
                    <LinkContainer to="/">
                        <Navbar.Brand>
                            <Image src={logo}  className="d-inline-block align-top" alt="logo"/>
                        </Navbar.Brand>
                    </LinkContainer>
                    <Navbar.Toggle onClick={handleShow} />
                    <Navbar.Collapse id="responsive-navbar-nav">
                        <Nav className="ms-auto">
                            <LinkContainer to="#">
                                <Nav.Link>Home</Nav.Link>
                            </LinkContainer>
                            <LinkContainer to="#">
                                <Nav.Link>About Us</Nav.Link>
                            </LinkContainer>
                            <LinkContainer to="#">
                                <Nav.Link>Contact</Nav.Link>
                            </LinkContainer>
                        </Nav>
                    </Navbar.Collapse>
                </Container>
            </Navbar>

            <Offcanvas show={show} onHide={handleClose}>
            <Offcanvas.Header closeButton>
            <Offcanvas.Title>
                <Image src={logo}  className="d-inline-block align-top" alt="logo"/>
            </Offcanvas.Title>
            </Offcanvas.Header>
            <Offcanvas.Body>
                <Nav  className="flex-column">
                    <LinkContainer to="#">
                        <Nav.Link>Home</Nav.Link>
                    </LinkContainer>
                    <LinkContainer to="#">
                        <Nav.Link>About Us</Nav.Link>
                    </LinkContainer>
                    <LinkContainer to="#">
                        <Nav.Link>Contact</Nav.Link>
                    </LinkContainer>
                </Nav>
            </Offcanvas.Body>
            </Offcanvas>
        </>
    )
}

export default Header

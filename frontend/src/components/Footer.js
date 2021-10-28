import React from 'react'
import { Row, Col, Container } from 'react-bootstrap'

function Footer() {
    const today = new Date();

    return (
        <>
            <div className="py-3 bg-secondary">
                <Container>
                    <Row>
                        <Col>
                            <h5>Product</h5>
                            <ul>
                                <li>The first choice</li>
                                <li>The first choice</li>
                                <li>The first choice</li>
                            </ul>
                        </Col>
                        <Col>The first choice</Col>
                        <Col>The first choice</Col>
                        <Col>The first choice</Col>
                    </Row>
                    <Row className="py-2">
                        <p class="mb-1">Made with Django Framework. <b>SnapSolar Engineering</b>  &copy; 2021 - {today.getFullYear()} | All Right Reserver</p>
                    </Row>
                </Container>
            </div>
        </>
    )
}

export default Footer

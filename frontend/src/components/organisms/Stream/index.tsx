import React from 'react'
import { Button, Card, Col, Row, Skeleton, Space, Typography, notification } from 'antd';
import { RobotOutlined } from '@ant-design/icons'
import { Link, useParams, useNavigate, Route, Routes } from "react-router-dom";

import { useStream } from '../../../hooks/useStream'
import PageColumn from '../../templates/PageColumn';
import BotForm from '../../organisms/BotForm'
import BotList from '../../molecules/BotList'
import Bot from '../Bot';

const Stream = () => {
    let { streamId } = useParams();
    const navigate = useNavigate();

    const { stream, loading, error, createBot } = useStream({ id: streamId as string })

    return (
        <Row gutter={16}>
            <Col span={8}>
                <PageColumn
                    header={[
                        <Typography.Text strong>Stream</Typography.Text>
                    ]}
                >
                    <Card bordered>
                        <Skeleton loading={loading} avatar paragraph={{ rows: 0 }}>
                            <Card.Meta
                                title={stream?.name}
                                description={
                                    <Row justify='space-between' align='bottom'>
                                        <Col>
                                            <Space>
                                                <Typography.Text>{stream?.botSet.edges.length} x</Typography.Text>
                                                <RobotOutlined />
                                            </Space>
                                        </Col>
                                        <Col>
                                            <Link to="https://speckle.xyz/streams/87a17f4280">
                                                <Button>Speckle Stream</Button>
                                            </Link>
                                        </Col>
                                    </Row>

                                }
                            />
                        </Skeleton>
                    </Card>
                </PageColumn>
            </Col>
            <Col span={16}>
                <Routes>
                    <Route index element={
                        <PageColumn
                            header={[
                                <Typography.Text strong>Bots</Typography.Text>,
                                <Link to={`/streams/${streamId}/new`}>
                                    <Button
                                        type="primary" size="small"
                                    >
                                        New Bot
                                    </Button>
                                </Link>
                            ]}
                        >
                            <BotList />
                        </PageColumn>
                    } />
                    <Route path="new" element={(
                        <PageColumn
                            header={[
                                <Typography.Text strong>New Bot</Typography.Text>,
                                <Link to={`/streams/${streamId}`}>
                                    <Button
                                        type="primary" size="small"
                                    >
                                        Back
                                    </Button>
                                </Link>
                            ]}
                        >
                            <Card>
                                <BotForm
                                    buttonText='Create Bot'
                                    onFinish={async (values) => {
                                        return createBot(values).then(() => {
                                            navigate(`/streams/${streamId}`)
                                        }).catch((e) => {
                                            notification.error({
                                                message: 'Error creating bot',
                                                description: e.message
                                            })
                                        })
                                    }}
                                />
                            </Card>
                        </PageColumn>
                    )} />
                    <Route path=":botId" element={
                        <PageColumn
                            header={[
                                <Typography.Text strong>Bot</Typography.Text>,
                                <Link to={`/streams/${streamId}`}>
                                    <Button
                                        type="primary" size="small"
                                    >
                                        Back
                                    </Button>
                                </Link>
                            ]}
                        >
                            <Bot />
                        </PageColumn>
                    } />
                </Routes>
            </Col>
        </Row>
    )
}

export default Stream
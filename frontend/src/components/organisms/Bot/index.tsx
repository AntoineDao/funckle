import { Button, Card, Skeleton, Typography } from 'antd';
import React, { useState } from 'react'
import { notification, Row, Col } from 'antd';
import { useParams, useNavigate } from "react-router-dom";

import { useBot } from '../../../hooks/useBot';
import LogViewer from '../../atoms/LogViewer';
import BotMeta from '../../molecules/BotMeta';
import BotForm from '../BotForm';


const Bot = () => {
    let { botId } = useParams();

    const { bot, botLogs, loading, error, updateBot, deleteBot, refetch } = useBot({ id: botId as string })

    const [tab, setTab] = useState('settings')

    const tabs = {
        'settings': (
            <BotForm
                buttonText='Update Bot'
                onFinish={async (values) => {
                    return updateBot(values).then(() => {
                        refetch()
                    }).catch((e) => {
                        notification.error({
                            message: 'Error updating bot',
                            description: e.message
                        })
                    })
                }}
                initialValues={{
                    slug: bot?.slug,
                    description: bot?.description,
                    functionVersionId: bot?.functionVersion.id,
                    triggers: bot?.triggers,
                    environmentVariables: bot?.environmentVariables,
                    secretEnvironmentVariables: bot?.secretEnvironmentVariables,
                }}
            />
        ),
        'logs': (
            <Row>
                <Col span={24}>
                    <Typography.Title level={5}>Bot Logs</Typography.Title>
                </Col>
                <Col span={24}>
                    <Typography.Text type='secondary'>
                        Logs are updated every 5 seconds and are limited to the last hour.
                    </Typography.Text>
                </Col>
                <Col span={24}>
                    <Card bordered={false} >
                        <Card.Grid
                            hoverable={false}
                            style={{
                                width: '100%', overflow: 'auto',
                                maxHeight: '100vh', padding: '0px',
                                boxShadow: 'none'
                            }}>
                            <LogViewer logs={botLogs} />
                        </Card.Grid>
                    </Card>
                </Col>
            </Row>

        )
    }


    return (
        <Card
            loading={loading}
            title={
                <Skeleton loading={loading} title={false} paragraph={{ rows: 1 }}>
                    {bot && <BotMeta {...bot} />}
                </Skeleton>
            }
            tabList={[
                { 'key': 'settings', 'tab': 'Settings' },
                { 'key': 'logs', 'tab': 'Live Logs' },
            ]}
            activeTabKey={tab}
            onTabChange={setTab}
            actions={[
                <Button danger onClick={() => {
                    deleteBot(botId as string)
                }}>
                    Delete Bot
                </Button>
            ]}
        >
            {/* @ts-ignore */}
            {tabs[tab]}
        </Card >
    )
}

export default Bot
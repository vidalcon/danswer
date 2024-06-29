import React, { useState } from 'react';
import { Modal } from "@/components/Modal";
import { Button, Text, Callout } from "@tremor/react";

import { Label } from "@/components/admin/connectors/Field";
import { CloudEmbeddingProvider } from '../components/types';



export function ChangeCredentialsModal({
    provider,
    onConfirm,
    onCancel,
}: {
    provider: CloudEmbeddingProvider;
    onConfirm: (apiKey: string) => void;
    onCancel: () => void;
}) {
    const [apiKey, setApiKey] = useState('');

    return (
        <Modal title={`Swap Keys for ${provider.name}`} onOutsideClick={onCancel}>
            <div className="mb-4">
                <Text className="text-lg mb-2">
                    Ready to play key swap with {provider.name}? Your old key is about to hit the bit bucket.
                </Text>
                <Callout title="Read the Fine Print" color="blue" className="mt-4">
                    <div className="flex flex-col gap-y-2">
                        <p>This isn&apos;t just a local change. Every model tied to this provider will feel the ripple effect.</p>
                        <Label>Your Shiny New API Key</Label>
                        <input
                            type="password"
                            className="text-lg w-full p-1"
                            value={apiKey}
                            onChange={(e) => setApiKey(e.target.value)}
                            placeholder="Paste your 1337 API key here"
                        />
                        <a href={provider.apiLink} target="_blank" rel="noopener noreferrer" className="underline cursor-pointer">
                            RTFM: {provider.name} API key edition
                        </a>
                    </div>
                </Callout>
                <Text className="text-sm mt-4">
                    Fun fact: This key swap could save you up to 15% on your API calls. Or not. We&apos;re developers, not fortune tellers.
                </Text>
                <div className="flex mt-8 justify-between">
                    <Button color="gray" onClick={onCancel}>Abort Key Swap</Button>
                    <Button color="blue" onClick={() => onConfirm(apiKey)} disabled={!apiKey}>
                        Execute Key Swap
                    </Button>
                </div>
            </div>
        </Modal>
    );
}
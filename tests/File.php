<?php
namespace Test\Followupemail2\Model;

use Test\Test\Api\Data\CampaignInterface;
use Test\Test\Api\Data\CampaignExtensionInterface;
use Test\Test\Model\ResourceModel\Campaign as CampaignResource;
use Magento\Framework\Model\AbstractModel;

/**
 * Class Campaign
 * @package Aheadworks\Followupemail2\Model
 * @codeCoverageIgnore
 */
class Campaign extends AbstractModel implements CampaignInterface
{
    /**
     * {@inheritdoc}
     */
    protected function _construct()
    {
        $this->_init(CampaignResource::class);
    }

    /**
     * {@inheritdoc}
     */
    public function getId()
    {
        return $this->getData(self::ID);
    }

    /**
     * {@inheritdoc}
     */
    public function setId($campaignId)
    {
        return $this->setData(self::ID, $campaignId);
    }
}